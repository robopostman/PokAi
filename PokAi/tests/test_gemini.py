import os
import unittest
from unittest.mock import Mock, patch

import requests

from ask_gemini import ask_gemini


class AskGeminiTests(unittest.TestCase):
    @patch("ask_gemini.load_dotenv")
    @patch("ask_gemini.requests.post")
    def test_uses_current_default_model(self, post: Mock, _load_dotenv: Mock) -> None:
        response = Mock()
        response.json.return_value = {
            "candidates": [{"content": {"parts": [{"text": "Hello"}]}}]
        }
        post.return_value = response

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True):
            self.assertEqual(ask_gemini("Say hello"), "Hello")

        self.assertIn(
            "/models/gemini-3.6-flash:generateContent",
            post.call_args.args[0],
        )

    @patch("ask_gemini.load_dotenv")
    @patch("ask_gemini.requests.post")
    def test_http_error_includes_gemini_error_details(
        self, post: Mock, _load_dotenv: Mock
    ) -> None:
        response = Mock()
        response.status_code = 404
        response.text = '{"error":{"message":"Model not found"}}'
        response.raise_for_status.side_effect = requests.HTTPError(
            "404 Client Error"
        )
        post.return_value = response

        with patch.dict(os.environ, {"GEMINI_API_KEY": "test-key"}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "Model not found"):
                ask_gemini("Say hello")


if __name__ == "__main__":
    unittest.main()
