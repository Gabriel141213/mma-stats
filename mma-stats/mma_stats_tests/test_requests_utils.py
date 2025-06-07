import pytest
from unittest.mock import patch, MagicMock
from mma_stats.utils.requests_utils import retry_on_failure, make_request, rate_limit
import requests
import time

def test_retry_on_failure_success():
    @retry_on_failure(max_retries=3)
    def success_function():
        return "success"
    
    assert success_function() == "success"

def test_retry_on_failure_fails():
    @retry_on_failure(max_retries=3, delay=0)
    def failing_function():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        failing_function()

def test_rate_limit():
    start_time = time.time()
    
    @rate_limit
    def test_function():
        return "done"
    
    result = test_function()
    elapsed_time = time.time() - start_time
    
    assert result == "done"
    assert elapsed_time >= 1.0  # Assuming REQUEST_DELAY = 1

def test_make_request_success():
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        response = make_request("http://test.com")
        assert response == mock_response

def test_make_request_failure():
    with patch('requests.get') as mock_get:
        mock_get.side_effect = requests.exceptions.RequestException
        
        with pytest.raises(requests.exceptions.RequestException):
            make_request("http://test.com") 