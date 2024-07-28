from airflow import DAG  # type:ignore
from airflow.operators.python_operator import PythonOperator  # type: ignore
from datetime import datetime
from airflow.models import Variable  # type: ignore

filename = __file__.split("/")[-1].replace(".py", "")


dag = DAG(
    filename,
    description="Recuperando variáveis de ambiente",
    schedule_interval=None,
    start_date=datetime(2023, 3, 5),
    catchup=False,
    tags=["exemplos"],
)


def print_variable(**context):
    minha_var = Variable.get("myfirstpetname")
    print(f"O valor da variável é: {minha_var}")


task1 = PythonOperator(task_id="tsk1", python_callable=print_variable, dag=dag)

task1
