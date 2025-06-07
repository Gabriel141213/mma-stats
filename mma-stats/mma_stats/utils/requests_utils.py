import logging
import time
from functools import wraps
from typing import Callable, Any
import requests
from ..constants import REQUEST_DELAY

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def retry_on_failure(max_retries: int = 3, delay: int = 1) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if retries == max_retries:
                        raise
                    logging.warning(f"Tentativa {retries} falhou: {e}. Tentando novamente...")
                    time.sleep(delay * retries)
            return None
        return wrapper
    return decorator

def rate_limit(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        time.sleep(REQUEST_DELAY)
        return func(*args, **kwargs)
    return wrapper

@rate_limit
def make_request(url: str) -> requests.Response:
    response = requests.get(url)
    response.raise_for_status()
    return response