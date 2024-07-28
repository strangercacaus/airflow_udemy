from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.python_operator import PythonOperator  # type: ignore
from datetime import datetime

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Dag que utiliza o Xcom para troca de dados",
    schedule_interval=None,
    start_date=datetime(2027, 7, 24),
    catchup=False,
    tags=["exemplos"],
)


def task_write(**kwargs):
    kwargs["ti"].xcom.push(key="valorxcom1", value=10200)


def task_read(**kwargs):
    valor = kwargs["ti"].xcom.pull(key="valorxcom1")
    print(f"Valor recuperado : {valor}")


task1 = PythonOperator(task_id="tsk1", python_callable=task_write, dag=dag)

task2 = PythonOperator(task_id="tsk2", python_callable=task_read, dag=dag)

task1 >> task2
