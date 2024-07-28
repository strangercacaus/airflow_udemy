# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime
from airflow.operators.dagrun_operator import TriggerDagRunOperator

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Dag run dag",
    schedule_interval=None,
    start_date=datetime(2024, 7, 22),
    catchup=False
)

task1 = BashOperator(task_id="tsk1", bash_command="sleep 5", dag=dag)
task2 = TriggerDagRunOperator(task_id="tsk2", trigger_dag_id="exemplo_triggerdagrun_operator_2", dag=dag)


task1 >> task2
