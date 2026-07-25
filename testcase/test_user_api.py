from typing import Any

import pytest

from common.http_client import HttpClient


USER_CASES: list[dict[str, Any]] = [
    {
        "case_name": "Get active user",
        "user_id": 1,
        "expected_status_code": 200,
        "expected_body": {
            "id": 1,
            "name": "Xinrui",
            "active": True,
        },
    },
    {
        "case_name": "Get inactive user",
        "user_id": 2,
        "expected_status_code": 200,
        "expected_body": {
            "id": 2,
            "name": "Mika",
            "active": False,
        },
    },
    {
        "case_name": "Get missing user",
        "user_id": 999,
        "expected_status_code": 404,
        "expected_body": {
            "detail": "User not found",
        },
    },
]


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