from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from datetime import datetime

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Usa tanto os operadores bitwise (>>) quanto o método set_upstrtream e set_downstream.",
    schedule_interval=None,
    start_date=datetime(2024, 7, 22),
    catchup=False,
)

task1 = BashOperator(task_id="tsk1", bash_command="sleep 5", dag=dag)
task2 = BashOperator(task_id="tsk2", bash_command="sleep 10", dag=dag)
task3 = BashOperator(task_id="tsk3", bash_command="sleep 5", dag=dag)
task4 = BashOperator(task_id="tsk4", bash_command="sleep 5", dag=dag)
task5 = BashOperator(task_id="tsk5", bash_command="sleep 5", dag=dag)

task1 >> [task2, task3]
task4.set_upstream(task3)
task5.set_upstream(task3)
task5.set_upstream(task2)
