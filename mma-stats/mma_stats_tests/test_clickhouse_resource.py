import pytest
from unittest.mock import MagicMock, patch
from clickhouse_driver import Client
from dagster import build_init_resource_context
from mma_stats.resources.clickhouse_resource import clickhouse_resource

def test_clickhouse_resource_configuration():
    """Test if clickhouse resource is created with correct configuration"""
    context = build_init_resource_context(
        config={
            "host": "clickhouse",
            "port": 9000,
            "user": "default",
            "password": "",
            "database": "default"
        }
    )
    
    with patch('mma_stats.resources.clickhouse_resource.Client') as mock_client:
        with clickhouse_resource(context) as client:  # Use context manager properly
            mock_client.assert_called_once_with(
                host="clickhouse",
                port=9000,
                user="default",
                password="",
                database="default",
                settings={"use_numpy": True}
            ) 