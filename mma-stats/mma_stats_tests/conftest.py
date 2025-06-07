import pytest
from unittest.mock import MagicMock
import vcr

@pytest.fixture(scope="module")
def vcr_config():
    return {
        "filter_headers": ["authorization"],
        "record_mode": "once",
    }

@pytest.fixture
def mock_context():
    context = MagicMock()
    context.resource_config = {
        "host": "localhost",
        "port": 9000,
        "user": "default",
        "password": "",
        "database": "default"
    }
    return context 