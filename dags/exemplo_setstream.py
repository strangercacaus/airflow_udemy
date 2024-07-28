from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from datetime import datetime

filename = __file__.split("/")[-1].replace(".py", "")
with DAG(
    filename,
    description="Precedência e Sequência de Tasks com set_upstream e set_downstream",
    schedule_interval=None,
    start_date=datetime(2024, 7, 22),
    catchup=False,
    tags=["exemplos"],
) as dag:

    task1 = BashOperator(task_id="tsk1", bash_command="sleep 5")
    task2 = BashOperator(task_id="tsk2", bash_command="sleep 5")
    task3 = BashOperator(task_id="tsk3", bash_command="sleep 5")
    task1.set_downstream(task2)
    task3.set_upstream(task2)
