import os
from flask import Flask, jsonify, request
from prophet import Prophet
import pandas as pd
from db import get_sales
from google.cloud import storage
import json
from prophet.serialize import model_to_json, model_from_json

app = Flask(__name__)

model_bucket = os.environ.get('MODEL_BUCKET')
model_filename = os.environ.get('MODEL_FILENAME')

model = None

"""
    Clean up and transform sales history
    Returns:
        Dataframe with columns ['saletime', 'pricepaid']
"""
def _prepare_sales_data():
    sales = get_sales()
    if len(sales) > 0:
        sales_df = pd.DataFrame(sales, columns = ["salesid", "listid", "sellerid", "buyerid", "eventid", 
        "dateid", "qtysold", "pricepaid", "commission", "saletime"])
        sales_df['saletime'] = pd.to_datetime(sales_df['saletime'], infer_datetime_format=True)
        sales_df['pricepaid'] = sales_df['pricepaid'].fillna(0)
        return sales_df[['saletime', 'pricepaid']].copy()
    else:
        return 'No sales in DB'

"""
    Gets and loads the prediction model from the bucket
    Returns:
        None
"""
@app.before_first_request
def _load_model():
    global model
    client = storage.Client()
    bucket = client.get_bucket(model_bucket)
    blob = bucket.blob(model_filename)
    blob.download_to_filename(model_filename)
    with open(model_filename, 'r') as fin:
        model = model_from_json(json.load(fin))

"""
    Train the model with ALL sales history
    Returns:
        Json with message and status code
"""
@app.route('/sales/train', methods=['GET'])
def train_model_from_zero():
    df = _prepare_sales_data()
    if not isinstance(df, str):
        df = df.rename(columns={'saletime': 'ds', 'pricepaid': 'y'})
        df = df.groupby(by=["ds"]).sum().reset_index()
        m = Prophet(yearly_seasonality=True, seasonality_mode="multiplicative")
        m.fit(df)
        with open('serialized_model.json', 'w') as fout:
            json.dump(model_to_json(m), fout)

        client = storage.Client()
        bucket = client.get_bucket(model_bucket)
        blob = bucket.blob(model_filename)
        blob.upload_from_filename(model_filename)
        return jsonify({"msg": 'New model trained successfully.'}), 200
    else:
        return jsonify(df), 500

"""
    Makes the prediction for a certain number of days since the last day of the sales history
    Returns:
        List of [saletime, daily pricepaid forecast] pairs
"""
@app.route('/sales/predict', methods=['GET', 'POST'])
def predict():
    try:
        if not request.is_json:
            return jsonify({"msg": "Missing JSON in request"}), 400
        else:
            days = request.json['days']
            future = model.make_future_dataframe(periods=days)
            forecast = model.predict(future.tail(days))
            forecast['yhat'] = forecast['yhat'].astype(int)
            forecast['ds'] = forecast['ds'].dt.strftime('%Y-%m-%d')
            return jsonify(forecast[['ds', 'yhat']].values.tolist()), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 500


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)