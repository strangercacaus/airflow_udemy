# Domine Apache Airflow. https://www.eia.ai/
from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.email_operator import EmailOperator  # type: ignore
from datetime import datetime, timedelta

filename = __file__.split("/")[-1].replace(".py", "")

default_args = {
    "depends_on_past": False,
    "start_date": datetime(2023, 3, 5),
    "email": ["caue.ausec@gmail.com"],
    "email_on_failure": True,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(seconds=10),
}

dag = DAG(
    filename,
    description="Dag que envia um email quando uma tarefa falha",
    default_args=default_args,
    schedule_interval=None,
    start_date=datetime(2023, 3, 5),
    catchup=False,
    default_view="graph",
    tags=['exemplos'],
)

task1 = BashOperator(task_id="1-Bash", bash_command="sleep 1", dag=dag)
task2 = BashOperator(task_id="2-Bash", bash_command="sleep 1", dag=dag)
task3 = BashOperator(task_id="3-Bash", bash_command="sleep 1", dag=dag)
task4 = BashOperator(task_id="4-Bash", bash_command="exit 1", dag=dag)
task5 = EmailOperator(
    task_id="5-Email",
    to="caue.ausec@gmail.com",
    subject="Airflow Error",
    html_content=f"""<h3>Ocorreu um erro na Dag. </h3>
                                        <p>Dag: {filename}""",
    trigger_rule='one_failed',
    dag=dag,
)
task6 = BashOperator(task_id="6-Bash", bash_command="sleep 1", dag=dag, trigger_rule="none_failed")
task7 = BashOperator(task_id="7-Bash", bash_command="sleep 1", dag=dag, trigger_rule="none_failed")

[task1, task2] >> task3 >> task4 >> [task5, task6, task7]
