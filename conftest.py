from collections.abc import Generator
from urllib import response

import pytest

from common.http_client import HttpClient


@pytest.fixture
def http_client() -> Generator[HttpClient, None, None]:
    client = HttpClient()

    yield client

    client.close()


@pytest.fixture(autouse=True)
def reset_test_data(
    http_client: HttpClient,
) -> None:
    """
    Reset the test data before each test case.
    """
    response = http_client.post("/api/test/reset")

    assert response.status_code == 200