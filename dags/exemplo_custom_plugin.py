from airflow import DAG # type: ignore
from datetime import datetime
from csvoperator import CsvOperator # type: ignore

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Nossa Dag",
    schedule_interval=None,
    start_date=datetime(2024, 7, 28),
    catchup=False,
    tags=['exemplos'],
)

parquettask = CsvOperator(
    task_id="parquet_task",
    input_file_path="/opt/airflow/data/Churn_produced.csv",
    output_file_path="/opt/airflow/data/Churn_columnar",
    separator=";",
    output_file_type="parquet",dag=dag
)

jsontask = CsvOperator(
    task_id="json_task",
    input_file_path="/opt/airflow/data/Churn_produced.csv",
    output_file_path="/opt/airflow/data/Churn_columnar",
    separator=";",
    output_file_type="json",dag=dag
)

parquettask >> jsontask