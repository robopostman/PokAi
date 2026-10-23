import unittest
from unittest.mock import Mock

import requests

from api_client import APIClient


class APIClientTests(unittest.TestCase):
    def setUp(self) -> None:
        self.client = APIClient("https://api.example.com/v1", "test-token")
        self.response = Mock()
        self.response.json.return_value = {"ok": True}
        self.client.session.request = Mock(return_value=self.response)

    def test_get_uses_base_url_auth_and_query_parameters(self) -> None:
        result = self.client.get("items", params={"limit": 5})

        self.assertEqual(result, {"ok": True})
        self.client.session.request.assert_called_once_with(
            method="GET",
            url="https://api.example.com/v1/items",
            params={"limit": 5},
            json=None,
            timeout=10.0,
        )
        self.assertEqual(
            self.client.session.headers["Authorization"], "Bearer test-token"
        )
        self.response.raise_for_status.assert_called_once_with()

    def test_post_sends_json(self) -> None:
        self.client.post("items", json={"name": "example"})

        self.client.session.request.assert_called_once_with(
            method="POST",
            url="https://api.example.com/v1/items",
            params=None,
            json={"name": "example"},
            timeout=10.0,
        )

    def test_rejects_absolute_endpoint(self) -> None:
        with self.assertRaisesRegex(ValueError, "relative path"):
            self.client.get("https://other.example.com/items")

    def test_http_errors_are_not_suppressed(self) -> None:
        self.response.raise_for_status.side_effect = requests.HTTPError("bad response")

        with self.assertRaises(requests.HTTPError):
            self.client.get("items")


if __name__ == "__main__":
    unittest.main()
