from airflow import DAG  # type: ignore
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator  # type: ignore
from airflow.operators.email_operator import EmailOperator  # type: ignore
from airflow.sensors.filesystem import FileSensor  # type: ignore
from airflow.providers.postgres.operators.postgres import PostgresOperator  # type: ignore
from airflow.utils.task_group import TaskGroup  # type: ignore
from airflow.models import Variable # type: ignore
from datetime import datetime, timedelta
import json, os

filename = __file__.split("/")[-1].replace(".py", "")
filepath = Variable.get("path_file") # type: ignore
conn_id = "airflow_postgresql_connection"

default_args = {
    "depends_on_past": False,
    "email": ["caue.ausec@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG(
    filename,
    description="Dados da Turbina",
    schedule_interval="*/5 * * * *",
    start_date=datetime(2023, 1, 1),
    catchup=False,
    default_args=default_args,
    default_view="graph",
    tags= ['projeto'],
)

group_check_temp = TaskGroup("group_check_temp", dag=dag)
group_database = TaskGroup("group_database", dag=dag)

file_sensor_task = FileSensor(
    task_id="file_sensor_task",
    filepath=filepath,
    fs_conn_id="fs_default",
    poke_interval=10,
    dag=dag,
)


def process_file(**kwargs):
    with open(filepath) as file:
        data = json.load(file)
        kwargs["ti"].xcom_push(key="idtemp", value=data["idtemp"])
        kwargs["ti"].xcom_push(key="powerfactor", value=data["powerfactor"])
        kwargs["ti"].xcom_push(key="hydraulicpressure", value=data["hydraulicpressure"])
        kwargs["ti"].xcom_push(key="temperature", value=data["temperature"])
        kwargs["ti"].xcom_push(key="timestamp", value=data["timestamp"])
    os.remove(filepath)


get_data = PythonOperator(
    task_id="get_data",
    python_callable=process_file,
    provide_context=True,
    dag=dag,
)

create_table = PostgresOperator(
    task_id="create_table",
    postgres_conn_id=conn_id,
    sql="""create table if not exists generator_sensors (idtemp varchar, powerfactor varchar, hydraulicpressure varchar, temperature varchar, timestamp varchar)
    """,
    task_group=group_database,
    dag=dag,
)

insert_data = PostgresOperator(
    task_id="insert_date",
    postgres_conn_id=conn_id,
    parameters=(
        '{{ti.xcom_pull(task_ids="idtemp,key="idtemp")}}',
        '{{ti.xcom_pull(task_ids="get_data,key="powerfactor")}}',
        '{{ti.xcom_pull(task_ids="get_data,key="hydraulicpressure")}}',
        '{{ti.xcom_pull(task_ids="get_data,key="temperature")}}',
        '{{ti.xcom_pull(task_ids="get_data,key="timestamp")}}',
    ),
    sql="""INSERT INTO generator_sensors (idtemp,powerfactor,hydraulicpressure,temperature,timestamp) VALUES(%s,%s,%s,%s,%s)""",
    task_group=group_database,
    dag=dag,
)

send_email_alert = EmailOperator(
    task_id="send_email_alert",
    to="caue.ausec@gmail.com",
    subject="airflow_alert",
    html_content="""<h3> Alerta de Temperatura. </h3>
    <p>Dag: windturbine</p>
    """,
    task_group=group_check_temp,
    dag=dag,
)

send_email_normal = EmailOperator(
    task_id="send_email_normal",
    to="caue.ausec@gmail.com",
    subject="airflow_alert",
    html_content="""<h3> Temperaturas normais. </h3>
    <p>Dag: windturbine</p>
    """,
    task_group=group_check_temp,
    dag=dag,
)


def avalia_temp(**kwargs):
    number = float(kwargs["ti"].xcom_pull(task_ids="get_data", key="temperature"))
    return "group_check_temp.send_email_alert" if number >= 24 else "group_check_temp.send_email_normal"


check_temp_branch = BranchPythonOperator(
    task_id="check_temp_branch",
    python_callable=avalia_temp,
    provide_context=True,
    dag=dag,
    task_group=group_check_temp,
)


with group_check_temp:
    check_temp_branch >> [send_email_alert, send_email_normal]

with group_database:
    create_table >> insert_data

file_sensor_task >> get_data
get_data >> group_check_temp
get_data >> group_database
