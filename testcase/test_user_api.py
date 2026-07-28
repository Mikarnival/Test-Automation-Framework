from pathlib import Path
from typing import Any

import pytest

from common.http_client import HttpClient
from common.yaml_loader import load_yaml

PROJECT_ROOT = Path(__file__).resolve().parents[1]

USER_CASES = load_yaml(
    PROJECT_ROOT / "data" / "user_cases.yaml"
)

CREATE_USER_CASES = load_yaml(
    PROJECT_ROOT / "data" / "create_user_cases.yaml"
)

UPDATE_USER_CASES = load_yaml(
    PROJECT_ROOT / "data" / "update_user_cases.yaml"
)

DELETE_USER_CASES = load_yaml(
    PROJECT_ROOT / "data" / "delete_user_cases.yaml"
)


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


@pytest.mark.parametrize(
    "case",
    CREATE_USER_CASES,
    ids=[case["case_name"] for case in CREATE_USER_CASES],
)
def test_create_user(
    http_client: HttpClient,
    case: dict[str, Any],
) -> None:
    response = http_client.post(
        "/api/users",
        json=case["request_body"],
    )

    assert response.status_code == case["expected_status_code"]

    if "expected_body" in case:
        body = response.json()

        for key, expected_value in case["expected_body"].items():
            assert body[key] == expected_value

    if case.get("verify_created_user", False):
        created_user = response.json()
        user_id = created_user["id"]

        get_response = http_client.get(
            f"/api/users/{user_id}"
        )

        assert get_response.status_code == 200
        assert get_response.json() == created_user


@pytest.mark.parametrize(
    "case",
    UPDATE_USER_CASES,
    ids=[case["case_name"] for case in UPDATE_USER_CASES],
)
def test_update_user(
    http_client: HttpClient,
    case: dict[str, Any],
) -> None:
    response = http_client.put(
        f"/api/users/{case['user_id']}",
        json=case["request_body"],
    )

    assert response.status_code == case["expected_status_code"]

    if "expected_body" in case:
        assert response.json() == case["expected_body"]


def test_create_update_and_get_user(
    http_client: HttpClient,
) -> None:
    create_response = http_client.post(
        "/api/users",
        json={
            "name": "Original Name",
            "active": True,
        },
    )

    assert create_response.status_code == 201

    created_user = create_response.json()
    user_id = created_user["id"]

    update_payload = {
        "name": "Updated Name",
        "active": False,
    }

    update_response = http_client.put(
        f"/api/users/{user_id}",
        json=update_payload,
    )

    assert update_response.status_code == 200

    updated_user = update_response.json()

    assert updated_user == {
        "id": user_id,
        "name": "Updated Name",
        "active": False,
    }

    get_response = http_client.get(
        f"/api/users/{user_id}"
    )

    assert get_response.status_code == 200
    assert get_response.json() == updated_user


@pytest.mark.parametrize(
    "case",
    DELETE_USER_CASES,
    ids=[case["case_name"] for case in DELETE_USER_CASES],
)
def test_delete_user(
    http_client: HttpClient,
    case: dict[str, Any],
) -> None:
    response = http_client.delete(
        f"/api/users/{case['user_id']}"
    )

    assert response.status_code == case["expected_status_code"]

    if "expected_body" in case:
        assert response.json() == case["expected_body"]


def test_create_delete_and_get_user(
    http_client: HttpClient,
) -> None:
    create_response = http_client.post(
        "/api/users",
        json={
            "name": "Susu",
            "active": True,
        },
    )

    assert create_response.status_code == 201

    created_user = create_response.json()
    user_id = created_user["id"]

    delete_response = http_client.delete(
        f"/api/users/{user_id}"
    )

    assert delete_response.status_code == 200
    assert delete_response.json() == {"message": "User deleted"}

    get_response = http_client.get(
        f"/api/users/{user_id}"
    )

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "User not found",
    }
