from pathlib import Path
from decimal import Decimal

from common.product_client import ProductClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_get_all_products(product_client: ProductClient) -> None:
    response = product_client.get_products()

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 4

    product_ids = {product["id"] for product in products}
    expected_product_ids = {1, 2, 3, 4}

    assert product_ids == expected_product_ids


def test_get_product_by_category(product_client: ProductClient) -> None:
    response = product_client.get_products(category="food",)

    assert response.status_code == 200

    products = response.json()

    assert len(products) == 2

    assert all(
        product["category"] == "food"
        for product in products
    )


def test_get_product_with_unknow_category(product_client: ProductClient) -> None:
    response = product_client.get_products(category="unknown")

    assert response.status_code == 200
    assert response.json() == []


def test_get_product_by_min_price(product_client: ProductClient) -> None:
    response = product_client.get_products(min_price=Decimal("20.00"))

    assert response.status_code == 200

    products = response.json()

    assert all(
        Decimal(str(product["price"])) >= Decimal("20.00")
        for product in products
    )


def test_get_products_by_max_price(
    product_client: ProductClient,
) -> None:
    response = product_client.get_products(max_price=Decimal("20.00"))

    assert response.status_code == 200

    products = response.json()

    assert all(
        Decimal(str(product["price"])) <= Decimal("20.00")
        for product in products
    )


def test_get_products_with_combined_filters(
    product_client: ProductClient,
) -> None:
    response = product_client.get_products(
        category="food",
        min_price=Decimal("30.00"),
        max_price=Decimal("40.00"),
    )

    assert response.status_code == 200

    products = response.json()

    assert all(
        product["category"] == "food"
        and Decimal(str(product["price"])) >= Decimal("30.00")
        and Decimal(str(product["price"])) <= Decimal("40.00")
        for product in products
    )


def test_create_product_with_zero_price(
    product_client: ProductClient,
) -> None:
    payload = {
        "name": "Free Cat Toy",
        "category": "toys",
        "price": "0.00",
        "stock": 5,
        "active": True,
    }

    response = product_client.create_product(payload)

    assert response.status_code == 201
    assert Decimal(str(response.json()["price"])) == Decimal("0.00")


def test_create_product_with_negative_price(
    product_client: ProductClient,
) -> None:
    payload = {
        "name": "Invalid Product",
        "category": "toys",
        "price": "-0.01",
        "stock": 5,
        "active": True,
    }

    response = product_client.create_product(payload)

    assert response.status_code == 422


def test_create_product_with_zero_stock(
    product_client: ProductClient,
) -> None:
    payload = {
        "name": "Out of Stock Cat Bed",
        "category": "beds",
        "price": "29.99",
        "stock": 0,
        "active": False,
    }

    response = product_client.create_product(payload)

    assert response.status_code == 201
    assert response.json()["stock"] == 0


def test_create_product_with_negative_stock(
    product_client: ProductClient,
) -> None:
    payload = {
        "name": "Invalid Product",
        "category": "food",
        "price": "10.00",
        "stock": -1,
        "active": True,
    }

    response = product_client.create_product(payload)

    assert response.status_code == 422


def test_create_product_with_empty_name(
    product_client: ProductClient,
) -> None:
    payload = {
        "name": "",
        "category": "food",
        "price": "10.00",
        "stock": 3,
        "active": True,
    }

    response = product_client.create_product(payload)

    assert response.status_code == 422


def test_create_product_without_category(
    product_client: ProductClient,
) -> None:
    payload = {
        "name": "Cat Food",
        "price": "10.00",
        "stock": 3,
        "active": True,
    }

    response = product_client.create_product(payload)

    assert response.status_code == 422


def test_get_products_with_invalid_price_range(
    product_client: ProductClient,
) -> None:
    response = product_client.get_products(
        min_price=Decimal("50.00"),
        max_price=Decimal("10.00"),
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "min_price cannot be greater than max_price",
    }


def test_create_update_and_get_product(
    product_client: ProductClient,
) -> None:
    create_payload = {
        "name": "Feefee's Old Toy",
        "category": "toys",
        "price": "9.99",
        "stock": 5,
        "active": True,
    }

    create_response = product_client.create_product(
        create_payload
    )

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    update_payload = {
        "name": "Feefee's New Toy",
        "category": "toys",
        "price": "15.99",
        "stock": 10,
        "active": False,
    }

    update_response = product_client.update_product(
        product_id,
        update_payload,
    )

    assert update_response.status_code == 200

    updated_product = update_response.json()

    assert updated_product["id"] == product_id
    assert updated_product["name"] == "Feefee's New Toy"
    assert Decimal(str(updated_product["price"])) == Decimal("15.99")
    assert updated_product["stock"] == 10
    assert updated_product["active"] is False

    get_response = product_client.get_product(product_id)

    assert get_response.status_code == 200
    assert get_response.json() == updated_product


def test_create_delete_and_get_product(
    product_client: ProductClient,
) -> None:
    payload = {
        "name": "Temporary Cat Toy",
        "category": "toys",
        "price": "5.99",
        "stock": 1,
        "active": True,
    }

    create_response = product_client.create_product(payload)

    assert create_response.status_code == 201

    product_id = create_response.json()["id"]

    delete_response = product_client.delete_product(product_id)

    assert delete_response.status_code == 200
    assert delete_response.json() == {
        "message": "Product deleted",
    }

    get_response = product_client.get_product(product_id)

    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Product not found",
    }


def test_get_missing_product(
    product_client: ProductClient,
) -> None:
    response = product_client.get_product(999)

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_update_missing_product(
    product_client: ProductClient,
) -> None:
    payload = {
        "name": "Missing Product",
        "category": "toys",
        "price": "10.00",
        "stock": 2,
        "active": True,
    }

    response = product_client.update_product(
        999,
        payload,
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


def test_delete_missing_product(
    product_client: ProductClient,
) -> None:
    response = product_client.delete_product(999)

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Product not found",
    }


