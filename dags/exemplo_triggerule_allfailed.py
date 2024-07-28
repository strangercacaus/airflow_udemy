from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from datetime import datetime

filename = __file__.split("/")[-1].replace(".py", "")
dag = DAG(
    filename,
    description="Trigger rule a nível de task com falha no bash command",
    schedule_interval=None,
    start_date=datetime(2024, 7, 22),
    catchup=False,
)

task1 = BashOperator(task_id="tsk1", bash_command="exit 1", dag=dag)
task2 = BashOperator(task_id="tsk2", bash_command="exit 4", dag=dag)
task3 = BashOperator(
    task_id="tsk3", bash_command="sleep 5", dag=dag, trigger_rule="all_failed"
)

[task1, task2] >> task3
