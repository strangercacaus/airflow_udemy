from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
import pandas as pd


class CsvOperator(BaseOperator):

    @apply_defaults
    def __init__(
        self,
        input_file_path,
        output_file_path,
        separator=",",
        output_file_type="parquet",
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)
        self.input_file_path = input_file_path
        self.output_file_path = output_file_path
        self.separator = separator
        self.output_file_type = output_file_type

    def execute(self, context):
        df = pd.read_csv(self.input_file_path, sep=self.separator)
        if self.output_file_type == "parquet":
            df.to_parquet(self.output_file_path + ".parquet")
        elif self.output_file_type == "json":
            df.to_json(self.output_file_path + ".json")
        else:
            raise ValueError(
                'Tipo de arquivo de saída inválido, tente um de "json", "parquet"'
            )
