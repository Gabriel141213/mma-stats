from dagster import resource, Field
from clickhouse_driver import Client


@resource(
    config_schema={
        "host": Field(str, is_required=True, description="Host do servidor ClickHouse."),
        "port": Field(int, default_value=9000, description="Porta do servidor ClickHouse."),
        "user": Field(str, default_value="default", description="Usuário para autenticação."),
        "password": Field(str, default_value="", description="Senha para autenticação."),
        "database": Field(str, default_value="default", description="Banco de dados a ser usado."),
    }
)
def clickhouse_resource(context):
    """
    Recurso para gerenciar a conexão com o ClickHouse.
    """
    client = Client(
        host=context.resource_config["host"],
        port=context.resource_config["port"],
        user=context.resource_config["user"],
        password=context.resource_config["password"],
        database=context.resource_config["database"]
    )
    context.log.info("Conexão com o ClickHouse criada.")

    # Retorna o cliente
    try:
        yield client
    finally:
        context.log.info("Encerrando conexão com o ClickHouse.")
