from airflow import DAG # type: ignore
from airflow.operators.bash_operator import BashOperator # type: ignore
from datetime import datetime

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Exemplo de gestão de recursos com pools",
    schedule_interval=None,
    start_date=datetime(2024, 7, 26),
    catchup=False
)

task1 = BashOperator(task_id='tsk1',bash_command='sleep 5',dag=dag, pool='exemplo_pool')
task2 = BashOperator(task_id='tsk2',bash_command='sleep 5',dag=dag, pool='exemplo_pool',priority_weight=5)
task3 = BashOperator(task_id='tsk3',bash_command='sleep 5',dag=dag, pool='exemplo_pool')
task4 = BashOperator(task_id='tsk4',bash_command='sleep 5',dag=dag, pool='exemplo_pool')
task5 = BashOperator(task_id='tsk5',bash_command='sleep 5',dag=dag, pool='exemplo_pool', priority_weight=10)