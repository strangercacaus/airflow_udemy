from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from datetime import datetime
from airflow.utils.task_group import TaskGroup # type: ignore
from airflow.operators.dagrun_operator import TriggerDagRunOperator # type: ignore

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Trigger task",
    schedule_interval=None,
    start_date=datetime(2024, 7, 22),
    catchup=False)

task1 = BashOperator(task_id="tsk1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tsk2", bash_command="sleep 5", dag=dag)

task1>>task2