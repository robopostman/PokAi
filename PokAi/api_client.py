import os
from typing import Any, Mapping
from urllib.parse import urljoin, urlsplit

import requests
from dotenv import load_dotenv


class APIClient:
    def __init__(
        self,
        base_url: str,
        api_key: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        parsed_base_url = urlsplit(base_url)
        if parsed_base_url.scheme not in {"http", "https"} or not parsed_base_url.netloc:
            raise ValueError("base_url must be an absolute HTTP or HTTPS URL")
        if timeout <= 0:
            raise ValueError("timeout must be greater than zero")

        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})
        if api_key:
            self.session.headers["Authorization"] = f"Bearer {api_key}"

    @classmethod
    def from_env(cls) -> "APIClient":
        load_dotenv()
        base_url = os.getenv("API_BASE_URL")
        if not base_url:
            raise RuntimeError("Set API_BASE_URL in your environment or .env file")

        return cls(base_url=base_url, api_key=os.getenv("API_KEY") or None)

    def request(
        self,
        method: str,
        endpoint: str,
        *,
        params: Mapping[str, object] | None = None,
        json: object | None = None,
    ) -> Any:
        parsed_endpoint = urlsplit(endpoint)
        if parsed_endpoint.scheme or parsed_endpoint.netloc:
            raise ValueError("endpoint must be a relative path")

        url = urljoin(f"{self.base_url}/", endpoint.lstrip("/"))
        response = self.session.request(
            method=method.upper(),
            url=url,
            params=params,
            json=json,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json()

    def get(
        self,
        endpoint: str,
        *,
        params: Mapping[str, object] | None = None,
    ) -> Any:
        return self.request("GET", endpoint, params=params)

    def post(self, endpoint: str, *, json: object) -> Any:
        return self.request("POST", endpoint, json=json)
