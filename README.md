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

# Steps for Project Reproduction (includes some explanations)

*Pre-requirements* 

[Google Cloud Platform](https://cloud.google.com/) account.

*Recommendation* 

Clone of the repo for easier reproduction.  

I used MINGW64 in Windows 10 as Bash. 

The reproduction of the project can be divided in the following steps:

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

Terraform:
- [Install it] (https://learn.hashicorp.com/tutorials/terraform/install-cli)
- Change default variables "project", "region", "BQ_DATASET" in `variables.tf` (the file contains descriptions explaining these variables)


Data Pipeline:
- Download of csv file using a bash operator using curl;



Transformations:
For this particular dataset it didn't make sense to use partitioning and clustering ([explanation])


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




