import json
from typing import Text

from rasa_sdk.knowledge_base.storage import InMemoryKnowledgeBase
import pandas as pd

class MysqlDatasource(InMemoryKnowledgeBase):
    def __init__(self):
        super().__init__('mysql')

    def load(self) -> None:
        from .data_source import engine

        def load_table(table_name):
            query = f"select * from {table_name}"
            df = pd.read_sql_query(query, engine)
            return json.loads(df.to_json(orient='records'))

        self.data = {'restaurant': load_table('restaurant'),
                     'hotel': load_table('hotel')}


