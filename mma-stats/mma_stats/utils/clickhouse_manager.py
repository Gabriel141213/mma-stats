from clickhouse_driver import Client
from typing import Any, Dict, List
from constants import UFC_ATHLETES_COLUMNS

class ClickhouseManager:
    def __init__(self,
                 host: str,
                 port: int = 9000,
                 user: str = "default",
                 password: str = "",
                 database: str = "default"
                ):
        """
        Inicializa a conexão com o ClickHouse.
        """
        self.client = Client(host=host, port=port, user=user, password=password, database=database)

    def create_table(self, table_name: str, columns: Dict[str, str], engine: str = "MergeTree", order_by: str = ""):
        """
        Cria uma tabela no ClickHouse.
        """
        cols = ", ".join(f"`{col}` {dtype}" for col, dtype in columns.items())
        order_clause = f"ORDER BY {order_by}" if order_by else ""
        query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({cols}) ENGINE = {engine} {order_clause}"
        self.client.execute(query)

    def select_data(self, table_name: str, conditions: str = "", fields: List[str] = None):
        """
        Seleciona dados de uma tabela.
        """
        fields_query = ", ".join(fields) if fields else "*"
        where_clause = f"WHERE {conditions}" if conditions else ""
        query = f"SELECT {fields_query} FROM `{table_name}` {where_clause}"
        return self.client.execute(query)

    def delete_data(self, table_name: str, conditions: str):
        """
        Deleta dados de uma tabela com base em condições.
        """
        if not conditions: 
            raise ValueError("Condições para DELETE não podem estar vazias.")
        query = f"DELETE FROM `{table_name}` WHERE {conditions}"
        self.client.execute(query)
