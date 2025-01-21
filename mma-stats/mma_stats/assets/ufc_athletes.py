from .. import constants
from ..scrappers.ufc_athletes_scrapper import UFCScraper
from ..resources.clickhouse_resource import clickhouse_resource
from dagster import asset, OpExecutionContext

import pandas as pd

BASE_URL = constants.BASE_ATHLETES_URL

@asset(
    required_resource_keys={"clickhouse"},
)
def ufc_athletes_data(context: OpExecutionContext) -> None:
    """
    Function to scrape all UFC athletes and insert them into the ClickHouse database.
    """

    database = "mma_stats_bronze"
    table_name = "ufc_athletes"
    engine = "MergeTree"
    order_by = "Athlete_ID"

    client = context.resources.clickhouse
    scraper = UFCScraper()

    create_db_query = f"""
        CREATE DATABASE IF NOT EXISTS {database}
    """
    client.execute(create_db_query)

    cols = ", ".join(f"`{col}` {dtype}" for col, dtype in constants.UFC_ATHLETES_COLUMNS.items())
    order_clause = f"ORDER BY {order_by}" if order_by else ""
    create_table_query = f"CREATE TABLE IF NOT EXISTS {database}.{table_name} ({cols}) ENGINE = {engine} {order_clause}"

    print(create_table_query)
    client.execute(create_table_query)

    delete_query = f"""
        ALTER TABLE {database}.{table_name}
        DELETE WHERE 1
    """
    client.execute(delete_query)

    athletes = scraper.scrape_all_athletes()

    athletes_data = [athlete.to_dict() for athlete in athletes]
    
    df = pd.DataFrame(athletes_data)

    client.insert_dataframe(f"INSERT INTO mma_stats_bronze.ufc_athletes VALUES", df)

    print(f"{len(df)} registros inseridos com sucesso!")
