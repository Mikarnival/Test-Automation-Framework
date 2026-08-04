from typing import Any

from decimal import Decimal

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
import uvicorn

from mock_server.data_store import (
    PRODUCTS,
    USERS,
    reset_products,
    reset_users,
)

app = FastAPI()


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    active: bool = True


class UpdateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    active: bool


class CreateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(ge=0)
    stock: int = Field(ge=0)
    active: bool = True


class UpdateProductRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=50)
    price: Decimal = Field(ge=0)
    stock: int = Field(ge=0)
    active: bool


@app.get(
    "/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
    "/api/users/{user_id}")
def get_user(user_id: int) -> dict[str, Any]:
    user = USERS.get(user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return user


@app.get(
    "/api/products/{product_id}")
def get_product(product_id: int) -> dict[str, Any]:
    product = PRODUCTS.get(product_id)

    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    return product


@app.get(
    "/api/products")
def get_products(
    category: str | None = None,
    min_price: Decimal | None = None,
    max_price: Decimal | None = None,
) -> list[dict[str, Any]]:
    if (
        min_price is not None
        and max_price is not None
        and min_price > max_price
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="min_price cannot be greater than max_price",
        )

    products = list(PRODUCTS.values())

    if category is not None:
        products = [p for p in products if p["category"] == category]

    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]

    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]

    return products


@app.post(
    "/api/users",
    status_code=status.HTTP_201_CREATED,
)
def create_user(request: CreateUserRequest) -> dict[str, Any]:
    new_user_id = max(USERS, default=0) + 1

    user = {
        "id": new_user_id,
        "name": request.name,
        "active": request.active,
    }

    USERS[new_user_id] = user
    return user


@app.post(
    "/api/products",
    status_code=status.HTTP_201_CREATED,
)
def create_product(request: CreateProductRequest) -> dict[str, Any]:
    new_product_id = max(PRODUCTS, default=0) + 1

    product = {
        "id": new_product_id,
        "name": request.name,
        "category": request.category,
        "price": request.price,
        "stock": request.stock,
        "active": request.active,
    }

    PRODUCTS[new_product_id] = product
    return product


@app.put(
    "/api/users/{user_id}")
def update_user(user_id: int, request: UpdateUserRequest) -> dict[str, Any]:
    if user_id not in USERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    updated_user = {
        "id": user_id,
        "name": request.name,
        "active": request.active,
    }

    USERS[user_id] = updated_user
    return updated_user


@app.put(
    "/api/products/{product_id}")
def update_product(product_id: int, request: UpdateProductRequest) -> dict[str, Any]:
    if product_id not in PRODUCTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    updated_product = {
        "id": product_id,
        "name": request.name,
        "category": request.category,
        "price": request.price,
        "stock": request.stock,
        "active": request.active,
    }

    PRODUCTS[product_id] = updated_product
    return updated_product


@app.delete(
    "/api/users/{user_id}")
def delete_user(user_id: int) -> dict[str, str]:
    if user_id not in USERS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    del USERS[user_id]

    return {
        "message": "User deleted",
    }


@app.delete(
    "/api/products/{product_id}")
def delete_product(product_id: int) -> dict[str, str]:
    if product_id not in PRODUCTS:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )

    del PRODUCTS[product_id]

    return {
        "message": "Product deleted",
    }


@app.post(
    "/api/test/reset")
def reset_test_data() -> dict[str, str]:
    reset_users()
    reset_products()

    return {
        "message": "Test data reset",
    }


if __name__ == "__main__":
    uvicorn.run(
        "mock_server.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
