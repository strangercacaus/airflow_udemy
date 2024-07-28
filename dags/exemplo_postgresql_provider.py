from airflow import DAG  # type: ignore
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator  # type: ignore
from airflow.providers.http.sensors.http import HttpSensor  # type: ignore
from airflow.providers.postgres.operators.postgres import PostgresOperator  # type: ignore
from datetime import datetime
import requests

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Exemplo de dag usando conexão com postgresql",
    schedule_interval=None,
    start_date=datetime(2024, 7, 26),
    catchup=False,
    tags=['exemplos'],
)


def get_result(ti):
    task_instance = ti.xcom_pull(task_ids='query_data')
    print("Resultado da consulta:")
    for xrow in task_instance:
        print(xrow)


create_table = PostgresOperator(
    task_id="create_table",
    postgres_conn_id="airflow_postgresql_connection",
    sql="create table if not exists teste(id int);",
    dag=dag,
)

insert_row = PostgresOperator(
    task_id="insert_row",
    postgres_conn_id="airflow_postgresql_connection",
    sql="insert into teste values(1)",
    dag=dag,
)

query_data = PostgresOperator(
    task_id="query_data",
    postgres_conn_id="airflow_postgresql_connection",
    sql="select * from teste",
    dag=dag,
)

print_result = PythonOperator(
    task_id="print_result",
    python_callable=get_result,
    provide_context=True,
    dag=dag
)

create_table >> insert_row >> query_data >> print_result
