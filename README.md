# San Francisco Fire Incidents Analysis

## Data Engineering Zoomcamp Project

This repository contains my project for the completion of [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by [DataTalks.Club](https://datatalks.club).

## Index
- [Problem Description](#problem-description)
- [Dataset](#dataset)
- [Technologies Used](#technologies-used)
- [Steps for Project Reproduction](#steps-for-project-reproduction)
- [Summary of DAG of Data Pipeline and decisions regarding transformations](#Summary-of-DAG-of-Data-Pipeline-and-decisions-regarding-transformations)
- [Dashboard](#dashboard)
- [Conclusion](#conclusion)

# Problem Description

A fire incident is defined as an incident involving smoke, heat, and flames. 

The purpose of this simple project was to analyse the fire incidents dataset from the city of San Francisco in the US and answer the following questions:

- Which battalion responded to more fire incidents?
- What was the total number of fire incidents recorded?
- How was the distribution of the number of fire incidents across time?
- Which month registered the highest number of fire incidents?
- Which battalion had the lowest average arrival time to the incidents?
- Which battalion had the lowest average incident resolution time?

The solution for these questions is in the conclusion!

Brief summary of the steps:
* Upload of csv data file into a Data Lake. 
* Convertion of data from csv to parquet, transformation using SQL and upload to Data Warehouse. 
* Creation of dashboard to analyse data and visualize results. 

# Dataset

The chosen dataset was the fire incidents data of the city of San Francisco in the US from 1-Jan-2003 to 22-April-2022. 

It includes a summary of each (non-medical) incident to which the SF Fire Department responded. Each incident record includes, the incident number, the battalion whihc responded to the incident, the incident date, the timestamp of alarm, arrival and closure of the incident, among others. 

It is available for [download as a csv file](https://data.sfgov.org/api/views/wr8u-xric/rows.csv?accessType=DOWNLOAD) and for [consultation](https://data.sfgov.org/Public-Safety/Fire-Incidents/wr8u-xric) where it is also provided a [data dictionary](https://data.sfgov.org/api/views/wr8u-xric/files/54c601a2-63f1-4b27-a79d-f484c620f061?download=true&filename=FIR-0001_DataDictionary_fire-incidents.xlsx). As of 24-April-2022, this dataset is updated daily.

# Technologies Used

For this project I decided to use the following tools:
- Infrastructure as code (IaC): Terraform
- Workflow orchestration: Airflow
- Containerization: Docker
- Data Lake: Google Cloud Storage (GCS)
- Data Warehouse: BigQuery
- Transformations: SQL (Pyspark will be used in the future with more time and one less technical error!) 
- Visualization: Google Data Studio

# Steps for Project Reproduction

**Recommendation:** Clone of the repo for easier reproduction and use MINGW64 in Windows 10 as Bash.  

## Step 1
Creation of a [Google Cloud Platform (GCP)](https://cloud.google.com/) account.

## Step 2: Setup of GCP 
- Creation of new GCP project. Attention: The Project ID is important. 
- Go to `IAM & Admin > Service accounts > Create service account`, provide a service account name and grant the roles `Viewer`, `BigQuery Admin`, `Storage Admin`, `Storage Object Admin`. 
- Download locally, rename it to `google_credentials.json`. 
- Store it in your home folder `$HOME/.google/credentials/`for easier access. 
- Set as the variable GOOGLE_APPLICATION_CREDENTIALS
```
export GOOGLE_APPLICATION_CREDENTIALS="<path/to/your/service-account-authkeys>.json"; 
```
- Activate the following API's:
   * https://console.cloud.google.com/apis/library/iam.googleapis.com
   * https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com

## Step 3: Creation of a GCP Infrastructure
- [Install Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli)
- Change default variables `project`, `region`, `BQ_DATASET` in `variables.tf` (the file contains descriptions explaining these variables)
- Run the following commands on bash:

```shell
# Initialize state file (.tfstate)
terraform init

# Check changes to new infra plan
terraform plan -var="project=<your-gcp-project-id>"

# Create new infra
terraform apply -var="project=<your-gcp-project-id>"
```
- Confirm in GCP console that the infrastructure was correctly created

## Step 4: Use of `DockerFile` and `Docker-Compose` structure to run Airflow.

### Execution

**0.** In `docker-compose.yaml`, change the environment variables `GCP_PROJECT_ID`,`GCP_GCS_BUCKET` and the line  `C:/Users/Gustavo/.google/credentials/:/.google/credentials:ro` regarding the volume to your own setup values. 

**1.** Build the image (may take several minutes). You only need to run this command if you modified the Dockerfile or the `requirements.txt` file or if the first time you run Airflow. 

```
docker-compose build
```
    
**2.** Initialize the configurations:

```
docker-compose up airflow-init
```
    
**3.** Run Airflow:

```
docker-compose up -d
```
    
**4.** Browse `localhost:8080` to access the Airflow web UI. The default credentials are `airflow`/`airflow` (not a production-ready setup). These can be modified by searching for `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD` inside the `docker-compose.yaml` file.

**5.** Turn on the DAG and trigger it on the web UI or wait for its scheduled run (once a day). After the run is completed, shut down the container by running the command:

```
docker-compose down
```

## Step 5: Development of a visualization using Datastudio
To create a dashboard like [this one](https://datastudio.google.com/s/j2PER0kkXhs), you need to use the data source `fire_used_variables` and `Add a field` (button on the bottom right corner) for the following fields:
- `incident_month` with the formula `MONTH(Incident_Date)`
- `avg_arrival_time_secs` with the formula `AVG(arrival_time_secs)`
- `avg_resolution_time_secs` with the formula `AVG(resolution_time_secs)`


# Summary of DAG of Data Pipeline and decisions regarding transformations



## Data Pipeline
- Download of csv file containing the data;
- Convertion of data from csv to parquet;
- Upload of data to bucket in google cloud storage (data lake);
- Load raw data to Bigquery - table `fire_external_table`;
- Load transformed data to Bigquery - table `fire_used_variables`;
- Delete used csv file (to free space in local storage)

## Transformations

The transformations made were the selection of certain columns and creation of new ones (time diferencies).

It is known that tables with less than 1 GB don't show significant improvement with partitioning and clustering; doing so in a small table could even lead to increased cost due to the additional metadata reads and maintenance needed for these features. 

As of 24-April-2022, the dataset has a size of ~ 207 mb, thus I only performed transformations such as adding new variables, and not partitioning and clustering. 

*Pratical example:*

Creating for example a clustered table by battalion...

```sql
CREATE OR REPLACE TABLE buoyant-valve-347911.fire_all.fire_battalion_clustered
Cluster BY
  Battalion AS
SELECT * FROM buoyant-valve-347911.fire_all.fire_external_table;
```

...makes the query consume more data...
![Dashboard](/imgs/clustered_table.jpg)

than performing it on the not clustered table.
![Dashboard](/imgs/normal_table.jpg)



# Dashboard

Take a look into the finished dashboard [here](https://datastudio.google.com/s/j2PER0kkXhs).

![Dashboard](/imgs/dashboard.PNG)


# Conclusion 

Solution for the questions:
- Which battalion responded to more fire incidents? **B02**
- What was the total number of fire incidents recorded? **587868**
- How was the distribution of the number of fire incidents across time? **Check graph on the dashboard**
- Which month registered the highest number of fire incidents? **January**
- Which battalion had the lowest average arrival time to the incidents? **B01**
- Which battalion had the lowest average incident resolution time? **B01**

*Useful information:*
The dataset used for providing these solutions contained fire incidents from 1-Jan-2003 until 22-Apr-2022. As of 24-April-2022, this dataset is updated daily. 



**A special thank you to [DataTalks.Club](https://datatalks.club) for providing this incredible course! Also, thank you to the amazing slack community!**




