from collections.abc import Generator

import pytest

from common.http_client import HttpClient
from common.product_client import ProductClient

@pytest.fixture
def http_client() -> Generator[HttpClient, None, None]:
    client = HttpClient()

    yield client

    client.close()


@pytest.fixture
def product_client(http_client: HttpClient) -> ProductClient:
    return ProductClient(http_client=http_client)


@pytest.fixture(autouse=True)
def reset_test_data(
    http_client: HttpClient,
) -> None:
    """
    Reset the test data before each test case.
    """
    response = http_client.post("/api/test/reset")

    assert response.status_code == 200