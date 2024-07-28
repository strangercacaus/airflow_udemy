from airflow import DAG  # type: ignore
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator  # type: ignore
from airflow.providers.http.sensors.http import HttpSensor  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore
import statistics as sts
import requests

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Exemplo de dag com Http Sensor",
    schedule_interval=None,
    start_date=datetime(2024, 7, 26),
    catchup=False,
    tags=['exemplos'],
)


def query_api():
    response = requests.get("https://baconipsum.com/api/?type=meat")
    print(response.text)


check_api = HttpSensor(
    task_id="check_api",
    http_conn_id="baconipsum_http_connection",
    endpoint="?type=meat-and-filler",
    poke_interval=1,
    timeout=5,
    dag=dag,
)

process_data = PythonOperator(
    task_id="process_data", python_callable=query_api, dag=dag
)

check_api >> process_data
