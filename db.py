import os
import pymysql

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

"""
    Handles Cloud SQL connection
    Returns:
        Connection Manager
"""
def connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        conn = pymysql.connect(user=db_user, password=db_password,
                            unix_socket=unix_socket, db=db_name)
        return conn
    except pymysql.MySQLError as e:
        print(e)

"""
    Gets the sales history from the database
    Returns:
        List of sales
"""
def get_sales():
    try:
        conn = connection()
        with conn.cursor() as cursor:
            result = cursor.execute('SELECT * FROM sales;')
            sales = cursor.fetchall()
        conn.close()
        return sales
    except Exception as e:
        return {"msg": str(e)}