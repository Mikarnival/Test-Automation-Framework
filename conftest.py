from collections.abc import Generator

import pytest

from common.http_client import HttpClient


@pytest.fixture
def http_client() -> Generator[HttpClient, None, None]:
    client = HttpClient()

    yield client

    client.close()