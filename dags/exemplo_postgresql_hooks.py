from airflow import DAG  # type: ignore
from airflow.operators.python_operator import PythonOperator  # type: ignore
from airflow.providers.postgres.hooks.postgres import PostgresHook  # type: ignore
from datetime import datetime

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Exemplo de dag usando hooks do postgresql",
    schedule_interval=None,
    start_date=datetime(2024, 7, 26),
    catchup=False,
)


def create_table():
    pg_hook = PostgresHook(postgres_conn_id="airflow_postgresql_connection")
    pg_hook.run("create table if not exists teste2(id int);", autocommit=True)


def insert_data():
    pg_hook = PostgresHook(postgres_conn_id="airflow_postgresql_connection")
    pg_hook.run("insert into teste2 values(2);", autocommit=True)


def query_data(**kwargs):
    pg_hook = PostgresHook(postgres_conn_id="airflow_postgresql_connection")
    records = pg_hook.get_records("select * from teste2")
    print(type(records))
    kwargs["ti"].xcom_push(key="query_result", value=records)


def print_data(ti):
    task_instance = ti.xcom_pull(key="query_result", task_ids="query_data")
    print("Dados da tabela:")
    for row in task_instance:
        print(row)


create_table_task = PythonOperator(
    task_id="create_table", python_callable=create_table, dag=dag
)
insert_data_task = PythonOperator(
    task_id="insert_data", python_callable=insert_data, dag=dag
)
query_data_task = PythonOperator(
    task_id="query_data", python_callable=query_data, dag=dag, provide_context=True
)
print_data_task = PythonOperator(
    task_id="print_data", python_callable=print_data, dag=dag, provide_context=True
)

create_table_task >> insert_data_task >> query_data_task >> print_data_task
