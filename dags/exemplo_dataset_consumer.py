from airflow import DAG, Dataset  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore

filename = __file__.split("/")[-1].replace(".py", "")

dataset = Dataset("/opt/airflow/data/Churn_produced.csv")

dag = DAG(
    filename,
    description="Consumindo Datasets com Python",
    schedule=[dataset],
    start_date=datetime(2024, 7, 26),
    catchup=False,
    tags=['exemplos'],
)

def duplicate_file():
    dataset = pd.read_csv('/opt/airflow/data/Churn_produced.csv',sep=";")
    dataset.to_csv('/opt/airflow/data/Churn_consumed.csv',sep=";")
    
task1 = PythonOperator(task_id='tsk1',python_callable=duplicate_file,dag=dag,provide_context=True)
