# San Francisco Fire Incidents Analysis

## Data Engineering Zoomcamp Project

This repository contains my project for the completion of [Data Engineering Zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp) by [DataTalks.Club](https://datatalks.club).

## Index
- [Problem Description](#problem-description)
- [Dataset](#dataset)
- [Technologies Used](#technologies-used)
- [Steps for Project Reproduction](#steps-for-project-reproduction)
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

It is available for [download as a csv file] and for [consultation] where it is also provided a [data dictionary]. As of 24 of April of 2022, this dataset is updated daily.

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

**Recommendation:** Clone of the repo for easier reproduction. Also, I used MINGW64 in Windows 10 as Bash.  

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
- [Install Terraform] (https://learn.hashicorp.com/tutorials/terraform/install-cli)
- Change default variables "project", "region", "BQ_DATASET" in `variables.tf` (the file contains descriptions explaining these variables)
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

**4.** Use of `DockerFile` and `Docker-Compose` structure to run Airflow.

### Execution
4.0. In `docker-compose.yaml`, change the environment variables `GCP_PROJECT_ID`,`GCP_GCS_BUCKET` and the line  `C:/Users/Gustavo/.google/credentials/:/.google/credentials:ro` regarding the volume to your own setup values. 

**1.** Build the image (may take several minutes). You only need to run this command if you modified the Dockerfile or the `requirements.txt` file or if the first time you run Airflow. 

    ```bash
    docker-compose build
    ```
    
**2.** Initialize the configurations:

    ```bash
    docker-compose up airflow-init
    ```
    
**3.** Run Airflow:

    ```bash
    docker-compose up -d
    ```
    
**4.** Browse `localhost:8080` to access the Airflow web UI. The default credentials are `airflow`/`airflow` (not a production-ready setup). These can be modified by searching for `_AIRFLOW_WWW_USER_USERNAME` and `_AIRFLOW_WWW_USER_PASSWORD` inside the `docker-compose.yaml` file.

**5.** Turn on the DAG and trigger it on the web UI or wait for its scheduled run (once a day). After the run is completed, shut down the container by running the command:

```bash
docker-compose down
```

**[Extra Explanations](./airflow/extraexplanations.md)** (Summary of DAG of Data Pipeline and decisions regarding transformations)

**5.**  

# Dashboard

![Dashboard](/imgs/dashboard.pdf)

I used Google Data Studio to create the dashboard. Take a look into the finished dashboard [here](DASHLINK).

# Conclusion 

Solution for the questions:
- Which battalion responded to more fire incidents?
- What was the total number of fire incidents recorded?
- How was the distribution of the number of fire incidents across time?
- Which month registered the highest number of fire incidents?
- Which battalion had the lowest average arrival time to the incidents?
- Which battalion had the lowest average incident resolution time?

Useful information: The dataset used for providing these solutions contained fire incidents from 1-Jan-2003 until 22-Apr-2022. As of 24 of April of 2022, this dataset is updated daily. 


**A special thank you to [DataTalks.Club](https://datatalks.club) for providing this incredible course! Also, thank you to the amazing slack community!**




