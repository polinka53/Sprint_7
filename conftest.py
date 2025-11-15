import pytest
from utils.client import ApiClient
from utils.endpoints import BASE_URL

pytest_plugins = ["fixtures.courier"]

@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

@pytest.fixture(scope="session")
def api(base_url):
    return ApiClient(base_url)