from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from datetime import datetime

filename = __file__.split("/")[-1].replace(".py", "")
dag = DAG(
    filename,
    description="Sequencia de Tasks com Bitwise Operators",
    schedule_interval=None,
    start_date=datetime(2024, 7, 22),
    catchup=False,
    tags=['exemplos'],
)

task1 = BashOperator(task_id="tsk1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tsk2", bash_command="sleep 5", dag=dag)
task3 = BashOperator(task_id="tsk3", bash_command="sleep 5", dag=dag)

task1 >> task2 >> task3
