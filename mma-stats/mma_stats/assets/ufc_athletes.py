from .. import constants
from ..scrappers.ufc_athletes_scrapper import UFCScraper
from ..scrappers.ufc_records_scrapper import UFCRecordsScraper
from ..handlers.ufc_athletes_handler import ufc_athletes_handler
from ..handlers.ufc_athletes_record_handler import ufc_athletes_record_handler
from dagster import asset, OpExecutionContext, AssetIn
import pandas as pd
import numpy as np

BASE_URL = constants.BASE_ATHLETES_URL

@asset(
    required_resource_keys={"clickhouse"},
)
def ufc_athletes_data(context: OpExecutionContext) -> list:
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

    cols = ", ".join(f"`{col}` {dtype}" for col, dtype in constants.UFC_ATHLETES_BRONZE_COLUMNS.items())
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

    return [athlete['Athlete_ID'] for athlete in athletes_data]

@asset(
    ins={"athletes_ids": AssetIn("ufc_athletes_data")},
    required_resource_keys={"clickhouse"},
)
def ufc_athletes_records_data(context: OpExecutionContext, athletes_ids: list) -> None:
    """
    Function to scrape all UFC athletes records and insert them into the ClickHouse database.
    """

    database = "mma_stats_bronze"
    table_name = "ufc_athletes_records"
    engine = "MergeTree"
 

    client = context.resources.clickhouse
    scraper = UFCRecordsScraper()

    cols = ", ".join(f"`{col}` {dtype}" for col, dtype in constants.UFC_ATHLETES_RECORDS_BRONZE_COLUMNS.items())
    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {database}.{table_name} 
        ({cols}) 
        ENGINE = {engine} 
        ORDER BY (`Athlete_ID`, `Opponent_ID`, `Fight_Date`)
    """

    print(create_table_query)
    client.execute(create_table_query)

    delete_query = f"""
        ALTER TABLE {database}.{table_name}
        DELETE WHERE 1
    """
    client.execute(delete_query)

    athletes_records = scraper.scrape_all_athletes_records(athletes_ids)

    records_data = [athletes_record.to_dict() for athletes_record in athletes_records]

    df = pd.DataFrame(records_data)

    client.insert_dataframe(f"INSERT INTO mma_stats_bronze.ufc_athletes_records VALUES", df)

    print(f"{len(df)} registros inseridos com sucesso!")


@asset(
    required_resource_keys={"clickhouse"},
    deps=[ufc_athletes_records_data],
)
def ufc_athletes_handled_data(context: OpExecutionContext) -> None:
    """
    Function to handle the UFC athletes data.
    """
    client = context.resources.clickhouse

    athletes_columns = constants.UFC_ATHLETES_BRONZE_COLUMNS.keys()
    athletes_query = "SELECT * FROM mma_stats_bronze.ufc_athletes"
    athletes = pd.DataFrame(client.execute(athletes_query), columns=athletes_columns)

    athletes = ufc_athletes_handler(athletes)

    database = "mma_stats_silver"
    table_name = "ufc_athletes"
    engine = "MergeTree"

    cols = ", ".join(f"`{col}` {dtype}" for col, dtype in constants.UFC_ATHLETES_SILVER_COLUMNS.items())

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {database}.{table_name} 
        ({cols}) 
        ENGINE = {engine} 
        ORDER BY (Athlete_ID)
    """
    client.execute(create_table_query)

    delete_query = f"""
        ALTER TABLE {database}.{table_name}
        DELETE WHERE 1
    """
    client.execute(delete_query)
    
    client.execute(f"INSERT INTO {database}.{table_name} VALUES", athletes.to_dict('records'))

    #client.insert_dataframe(f"INSERT INTO {database}.{table_name} VALUES", athletes)

    print(f"{len(athletes)} registros inseridos com sucesso!")


@asset(
    required_resource_keys={"clickhouse"},
    deps=[ufc_athletes_records_data],
)
def ufc_athletes_records_handled_data(context: OpExecutionContext) -> None:
    """
    Function to handle the UFC athletes data.
    """
    client = context.resources.clickhouse

    fights_columns = constants.UFC_ATHLETES_RECORDS_BRONZE_COLUMNS.keys()
    fights_query = "SELECT * FROM mma_stats_bronze.ufc_athletes_records"
    fights = pd.DataFrame(client.execute(fights_query), columns=fights_columns)

    fights = ufc_athletes_record_handler(fights)

    database = "mma_stats_silver"
    table_name = "ufc_athletes_records"
    engine = "MergeTree"

    cols = ", ".join(f"`{col}` {dtype}" for col, dtype in constants.UFC_ATHLETES_RECORDS_SILVER_COLUMNS.items())

    create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {database}.{table_name} 
        ({cols}) 
        ENGINE = {engine} 
        ORDER BY (Athlete_ID, Opponent_ID, Fight_Date)
    """
    client.execute(create_table_query)

    delete_query = f"""
        ALTER TABLE {database}.{table_name}
        DELETE WHERE 1
    """
    client.execute(delete_query)
    
    client.execute(f"INSERT INTO {database}.{table_name} VALUES", fights.to_dict('records'))

    print(f"{len(fights)} registros inseridos com sucesso!")