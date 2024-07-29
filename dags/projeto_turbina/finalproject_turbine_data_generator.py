import json, time
from airflow import DAG  # type: ignore
from airflow.operators.python_operator import PythonOperator  # type: ignore
from datetime import datetime
from random import uniform

filename = __file__.split("/")[-1].replace(".py", "")
dag = DAG(
    filename,
    description="DAG para a Geração de valores aleatórias no projeto final",
    schedule_interval=None,
    start_date=datetime(2024, 7, 22),
    catchup=False,
    tags=["projeto"],
)

# def generate_random_values():
#     power_factor = uniform(0.7, 1)
#     hidraulic_pressure = uniform(70, 80)
#     temperature = uniform(20, 25)
#     record = {
#         "powerfactor": str(power_factor),
#         "hydraulicpressure": str(hidraulic_pressure),
#         "temperature": str(temperature),
#         "timestamp": str(datetime.now()),
#     }

#     with open("/opt/airflow/data/Generator_data.json", "a") as file:
#         json.dump(record, file)
#         file.write('\n')  # Add a newline character after each JSON record


def generate_random_values():
    idtemp = 0
    while True:
        idtemp += 1
        dados_pf = uniform(0.7, 1)

        dados_hp = uniform(70, 80)

        dados_tp = uniform(20, 25)
        registro = {
            "idtemp": str(idtemp),
            "powerfactor": str(dados_pf),
            "hydraulicpressure": str(dados_hp),
            "temperature": str(dados_tp),
            "timestamp": str(datetime.now()),
        }

        with open("/opt/airflow/data/Generator_data.json", "w") as fp:
            json.dump(registro, fp)
        time.sleep(60)


task1 = PythonOperator(
    task_id="Generate_Random_Values", python_callable=generate_random_values, dag=dag
)
