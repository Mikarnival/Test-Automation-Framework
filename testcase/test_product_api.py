from pathlib import Path
from typing import Any
from decimal import Decimal


from common.http_client import HttpClient
from common.yaml_loader import load_yaml


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_get_all_product(http_client: HttpClient) -> None:
    response = http_client.get(
        "/api/products"
    )

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 4

    product_ids = {product["id"] for product in products}
    expected_product_ids = {1, 2, 3, 4}

    assert product_ids == expected_product_ids


def test_get_product_by_category(http_client: HttpClient) -> None:
    response = http_client.get(
        "/api/products",
        params={"category": "food"}
    )

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 2

    assert all(
        product["category"] == "food"
        for product in products
    )


def test_get_product_with_unknow_category(http_client: HttpClient) -> None:
    response = http_client.get(
        "/api/products",
        params={"category": "unknown"}
    )

    assert response.status_code == 200
    assert response.json() == []


def test_get_product_by_min_price(http_client: HttpClient) -> None:
    response = http_client.get(
        "/api/products",
        params={"min_price": 20.00}
    )

    assert response.status_code == 200

    products = response.json()

    assert all(
        Decimal(str(product["price"])) >= Decimal("20.00")
        for product in products
    )


def test_get_products_by_max_price(
    http_client: HttpClient,
) -> None:
    response = http_client.get(
        "/api/products",
        params={
            "max_price": "20.00",
        },
    )

    assert response.status_code == 200

    products = response.json()

    assert all(
        Decimal(str(product["price"])) <= Decimal("20.00")
        for product in products
    )


def test_get_products_with_combined_filters(
    http_client: HttpClient,
) -> None:
    response = http_client.get(
        "/api/products",
        params={
            "category": "food",
            "min_price": "10.00",
            "max_price": "20.00",
        },
    )

    assert response.status_code == 200

    products = response.json()

    assert all(
        product["category"] == "food"
        and Decimal(str(product["price"])) >= Decimal("10.00")
        and Decimal(str(product["price"])) <= Decimal("20.00")
        for product in products
    )


def test_create_product_with_zero_price(
    http_client: HttpClient,
) -> None:
    payload = {
        "name": "Free Cat Toy",
        "category": "toys",
        "price": "0.00",
        "stock": 5,
        "active": True,
    }

    response = http_client.post(
        "/api/products",
        json=payload,
    )

    assert response.status_code == 201
    assert Decimal(str(response.json()["price"])) == Decimal("0.00")


def test_create_product_with_negative_price(
    http_client: HttpClient,
) -> None:
    payload = {
        "name": "Invalid Product",
        "category": "toys",
        "price": "-0.01",
        "stock": 5,
        "active": True,
    }

    response = http_client.post(
        "/api/products",
        json=payload,
    )

    assert response.status_code == 422


def test_create_product_with_zero_stock(
    http_client: HttpClient,
) -> None:
    payload = {
        "name": "Out of Stock Cat Bed",
        "category": "beds",
        "price": "29.99",
        "stock": 0,
        "active": False,
    }

    response = http_client.post(
        "/api/products",
        json=payload,
    )

    assert response.status_code == 201
    assert response.json()["stock"] == 0


def test_create_product_with_negative_stock(
    http_client: HttpClient,
) -> None:
    payload = {
        "name": "Invalid Product",
        "category": "food",
        "price": "10.00",
        "stock": -1,
        "active": True,
    }

    response = http_client.post(
        "/api/products",
        json=payload,
    )

    assert response.status_code == 422


def test_create_product_with_empty_name(
    http_client: HttpClient,
) -> None:
    payload = {
        "name": "",
        "category": "food",
        "price": "10.00",
        "stock": 3,
        "active": True,
    }

    response = http_client.post(
        "/api/products",
        json=payload,
    )

    assert response.status_code == 422


def test_create_product_without_category(
    http_client: HttpClient,
) -> None:
    payload = {
        "name": "Cat Food",
        "price": "10.00",
        "stock": 3,
        "active": True,
    }

    response = http_client.post(
        "/api/products",
        json=payload,
    )

    assert response.status_code == 422


def test_get_products_with_invalid_price_range(
    http_client: HttpClient,
) -> None:
    response = http_client.get(
        "/api/products",
        params={
            "min_price": "50.00",
            "max_price": "10.00",
        },
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "min_price cannot be greater than max_price",
    }