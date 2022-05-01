import os
import logging

from datetime import datetime

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

from google.cloud import storage
#from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator 
#from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator
#from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
import pyarrow.csv as pv
import pyarrow.parquet as pq
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateExternalTableOperator, BigQueryInsertJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator


PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
BUCKET = os.environ.get("GCP_GCS_BUCKET")

dataset_url = "https://data.sfgov.org/api/views/wr8u-xric/rows.csv?accessType=DOWNLOAD"
dataset_file = "fire_incidents_{{ execution_date.strftime(\'%Y_%m\') }}.csv"
parquet_file = dataset_file.replace('.csv', '.parquet')
path_to_local_home = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")
clear_file = path_to_local_home +'/fire_incidents_*'

BIGQUERY_DATASET = os.environ.get("BIGQUERY_DATASET", 'fire_all')


def format_to_parquet(src_file):
    if not src_file.endswith('.csv'):
        logging.error("Can only accept source files in CSV format, for the moment")
        return
    table = pv.read_csv(src_file)
    pq.write_table(table, src_file.replace('.csv', '.parquet'))


# NOTE: takes 20 mins, at an upload speed of 800kbps. Faster if your internet has a better upload speed
def upload_to_gcs(bucket, object_name, local_file):
    """
    Ref: https://cloud.google.com/storage/docs/uploading-objects#storage-upload-object-python
    :param bucket: GCS bucket name
    :param object_name: target path & file-name
    :param local_file: source path & file-name
    :return:
    """
    # WORKAROUND to prevent timeout for files > 6 MB on 800 kbps upload speed.
    # (Ref: https://github.com/googleapis/python-storage/issues/74)
    storage.blob._MAX_MULTIPART_SIZE = 5 * 1024 * 1024  # 5 MB
    storage.blob._DEFAULT_CHUNKSIZE = 5 * 1024 * 1024  # 5 MB
    # End of Workaround

    client = storage.Client()
    bucket = client.bucket(bucket)

    blob = bucket.blob(object_name)
    blob.upload_from_filename(local_file)


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "retries": 1,
}

with DAG(
    dag_id="fire_data_dag_gcs_bq",
    schedule_interval="@daily",
    default_args=default_args,
    catchup=False,
    max_active_runs=1,
    tags=['DE-fire-proj'],
) as dag:

    download_dataset_task = BashOperator(
        task_id="download_dataset_task",
        bash_command=f"curl -sS {dataset_url} > {path_to_local_home}/{dataset_file}"
    )

    format_to_parquet_task = PythonOperator(
        task_id="format_to_parquet_task",
        python_callable=format_to_parquet,
        op_kwargs={
            "src_file": f"{path_to_local_home}/{dataset_file}",
        },
    )
    local_to_gcs_task = PythonOperator(
        task_id="local_to_gcs_task",
        python_callable=upload_to_gcs,
        op_kwargs={
            "bucket": BUCKET,
            "object_name": f"fire_raw/{parquet_file}",
            "local_file": f"{path_to_local_home}/{parquet_file}",
        },
    )

    bigquery_external_table_task = BigQueryCreateExternalTableOperator(
            task_id=f"bq_fire_external_table_task",
            table_resource={
                "tableReference": {
                    "projectId": PROJECT_ID,
                    "datasetId": BIGQUERY_DATASET,
                    "tableId": f"fire_external_table",
                },
                "externalDataConfiguration": {
                    "autodetect": "True",
                    "sourceFormat": "PARQUET",
                    "sourceUris": [f"gs://{BUCKET}/fire_raw/{parquet_file}"],
                },
            },
        )
    
    CREATE_BQ_QUERY = (
            f"CREATE OR REPLACE TABLE {BIGQUERY_DATASET}.fire_used_variables AS \
             SELECT Incident_Number, Battalion, Incident_Date, \
             TIMESTAMP_DIFF(Arrival_DtTm,Alarm_DtTm, SECOND) AS arrival_time_secs, \
             TIMESTAMP_DIFF(Close_DtTm,Arrival_DtTm, SECOND) AS resolution_time_secs \
             FROM {BIGQUERY_DATASET}.fire_external_table;"
        )

        
    bq_create_summary_table_job = BigQueryInsertJobOperator(
            task_id=f"bq_create_summary_table_task",
            configuration={
                "query": {
                    "query": CREATE_BQ_QUERY,
                    "useLegacySql": False,
                }
            }
        )
    
    cleanup_job= BashOperator(
        task_id='cleanup_csv',
        bash_command=f'rm {clear_file}'
    )


    download_dataset_task  >> format_to_parquet_task >> local_to_gcs_task >> bigquery_external_table_task
    bigquery_external_table_task >> bq_create_summary_table_job >> cleanup_job