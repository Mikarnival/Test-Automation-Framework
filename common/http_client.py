from typing import Any

import requests
from requests import Response
from requests.exceptions import RequestException

from conf.setting import API_TIMEOUT, BASE_URL


class HttpClient:
    def __init__(
        self,
        base_url: str = BASE_URL,
        timeout: float = API_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> Response:
        url = f"{self.base_url}/{path.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )
        except RequestException as exc:
            raise RuntimeError(
                f"HTTP request failed: {method.upper()} {url}"
            ) from exc

        return response

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            method="GET",
            path=path,
            params=params,
        )

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            method="POST",
            path=path,
            json=json,
        )

    def put(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            method="PUT",
            path=path,
            json=json,
        )

    def close(self) -> None:
        self.session.close()