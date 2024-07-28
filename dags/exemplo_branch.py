from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator  # type: ignore
from datetime import datetime
from random import randint

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Exemplo de gestão de recursos com pools",
    schedule_interval=None,
    start_date=datetime(2024, 7, 26),
    catchup=False,
    tags=['exemplos'],
)


def get_random_number():
    return randint(1, 100)

def assert_random_number(**context):
    number = context["task_instance"].xcom_pull(task_ids="acquire_random")
    return "even" if number % 2 == 0 else "odd"

task1 = PythonOperator(task_id="acquire_random",python_callable=get_random_number,dag=dag)
task2 = BranchPythonOperator(task_id="branch",python_callable=assert_random_number,provide_context=True,dag=dag)
task3 = BashOperator(task_id="odd", bash_command="echo 'Odd Number'", dag=dag)
task4 = BashOperator(task_id="even", bash_command="echo 'Even Number'", dag=dag)

task1 >> task2
task2 >> task3
task2 >> task4