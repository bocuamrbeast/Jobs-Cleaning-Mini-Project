import os
import sys
from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime

FILE_PATH = os.path.realpath(__file__)
DAG_FOLDER = os.path.dirname(FILE_PATH)
PROJECT_ROOT = os.path.dirname(DAG_FOLDER)
sys.path.insert(0, PROJECT_ROOT)

from etl.extract import extract_data
from etl.transform import transform_data
from etl.load import load_data

with DAG(
    dag_id = 'jobs_etl',
    start_date = datetime(2026, 2, 1),
    schedule = '@daily',
    catchup = False
) as dag:
    extract_task = PythonOperator(
        task_id = 'extract_data',
        python_callable = extract_data
    )

    transform_task = PythonOperator(
        task_id = 'transform_data',
        python_callable = transform_data
    )

    load_task = PythonOperator(
        task_id = 'load_data',
        python_callable = load_data
    )

    extract_task >> transform_task >> load_task