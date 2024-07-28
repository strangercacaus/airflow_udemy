from airflow import DAG  # type: ignore
from airflow.operators.bash_operator import BashOperator  # type: ignore
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator  # type: ignore
from datetime import datetime
import pandas as pd  # type: ignore
import statistics as sts

filename = __file__.split("/")[-1].replace(".py", "")

dag = DAG(
    filename,
    description="Exemplo de execução de scripts python",
    schedule_interval=None,
    start_date=datetime(2024, 7, 26),
    catchup=False,
    tags=['exemplos'],
)


def clean_data():
    dataset = pd.read_csv("/opt/airflow/data/Churn.csv", sep=";")
    dataset.columns = [
        "Id",
        "Score",
        "Estado",
        "Genero",
        "Idade",
        "Patrimonio",
        "Saldo",
        "Produtos",
        "TemCartao",
        "Ativo",
        "Salario",
        "Saiu",
    ]
    # Gênero
    dataset["Genero"].fillna("Masculino", inplace=True)
    dataset["Genero"] = dataset["Genero"].apply(lambda x: (x.upper()[0]))

    # Salário
    mediana = sts.median(dataset["Salario"])
    dataset["Salario"].fillna(mediana, inplace=True)

    # Idade
    mediana = sts.median(dataset["Idade"])
    dataset["Idade"].fillna(mediana, inplace=True)
    dataset.loc[(dataset["Idade"] < 0 | (dataset["Idade"] > 120)), "Idade"] = mediana

    # Remover Duplicados
    dataset.drop_duplicates(subset="Id", keep="first")

    # Gravar Resultado
    dataset.to_csv("/opt/airflow/data/churn_clean.csv", sep=";", index=False)


task1 = PythonOperator(task_id="clean_data", python_callable=clean_data, dag=dag)
