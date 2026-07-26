from pathlib import Path
from typing import Any

import pytest

from common.http_client import HttpClient
from common.yaml_loader import load_yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER_CASES = load_yaml(PROJECT_ROOT / "data" / "user_cases.yaml")

@pytest.mark.parametrize(
    "case",
    USER_CASES,
    ids=[case["case_name"] for case in USER_CASES],
)
def test_get_user(
    http_client: HttpClient,
    case: dict[str, Any],
) -> None:
    response = http_client.get(
        f"/api/users/{case['user_id']}"
    )

    assert response.status_code == case["expected_status_code"]
    assert response.json() == case["expected_body"]