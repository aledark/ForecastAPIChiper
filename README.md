# Flask App
Python Flask application for time series forecasting on Google Cloud using App Engine, Cloud SQL and Cloud Storage.

### Create A Cloud SQL Instance
After signing up for Google Cloud, go to Cloud SQL and create a MySQL [instance](https://cloud.google.com/sql/docs/mysql/create-instance#console). 
Then, follow the steps below:
* [Create a database](https://cloud.google.com/sql/docs/mysql/create-manage-databases): tickitdb
* [Create a new user](https://cloud.google.com/sql/docs/mysql/create-manage-users)
* Connect to the instance: 
For this, navigate to the “Overview” panel and connect using the cloud shell. The command to connect to the Cloud SQL instance will be pre-typed in the console. Finally, enter the following commands on the console:
```
gcloud sql connect flask-demo --user=USERNAME
use tickitdb;
```
Now you can create the necessary tables by entering the respective SQL, for example:
```
create table categories(
catid SMALLINT NOT NULL AUTO_INCREMENT,
catgroup VARCHAR(10),
catname VARCHAR(10),
catdesc VARCHAR(50),
PRIMARY KEY(catid)
);
```
To populate the tables, you can easily do this by uploading the data files to a bucket and following [this steps](https://cloud.google.com/sql/docs/mysql/import-export/import-export-csv#console_1).

### Upload to App Engine Flex
First, clone this codebase:
```
git clone https://github.com/aledark/ForecastAPIChiper.git
```
Before we dive into the deployment of our API on App Engine, it is important to know about the repository structure:
* requirements.txt : contains a list of packages required to run the application. App Engine checks this file and installs the packages from the list.
* app.yaml: this has all the configuration that GCP needs such as Python version, SQL config, environment variables, etc.
* main.py, bd.py: API scripts.

Lastly, you need to [install](https://cloud.google.com/sdk/docs/quickstart-windows) the google cloud SDK on the machine (in this case windows), after configuring it, run the following command to deploy your app (within the root directory): 

```
gcloud app deploy
```

### API Documentation
You can find it by clicking [here](https://documenter.getpostman.com/view/11478617/UVsEV9Pm)
