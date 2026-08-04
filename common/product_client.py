from decimal import Decimal
from typing import Any

from requests import Response

from common.http_client import HttpClient

class ProductClient:
    def __init__(self, http_client: HttpClient):
        self.http_client = http_client

    def get_product(self, product_id: int | str) -> Response:
        return self.http_client.get(
            f"/api/products/{product_id}"
        )

    def get_products(
        self,
        category: str | None = None,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
    ) -> Response:
        params: dict[str, Any] = {}

        if category is not None:
            params["category"] = category

        if min_price is not None:
            params["min_price"] = str(min_price)

        if max_price is not None:
            params["max_price"] = str(max_price)

        return self.http_client.get(
            "/api/products",
            params=params,
        )

    def create_product(self, product_data: dict[str, Any]) -> Response:
        return self.http_client.post(
            "/api/products",
            json=product_data,
        )

    def update_product(self, product_id: int | str, product_data: dict[str, Any]) -> Response:
        return self.http_client.put(
            f"/api/products/{product_id}",
            json=product_data,
        )

    def delete_product(self, product_id: int | str) -> Response:
        return self.http_client.delete(
            f"/api/products/{product_id}"
        )