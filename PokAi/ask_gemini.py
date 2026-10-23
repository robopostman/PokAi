import os

import requests
from dotenv import load_dotenv


def ask_gemini(prompt: str) -> str:
    if not prompt.strip():
        raise ValueError("Prompt cannot be empty")

    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY in your environment or .env file")

    model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    response = requests.post(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent",
        headers={"x-goog-api-key": api_key},
        json={"contents": [{"parts": [{"text": prompt}]}]},
        timeout=30,
    )
    try:
        response.raise_for_status()
    except requests.HTTPError as error:
        raise RuntimeError(
            f"Gemini API returned HTTP {response.status_code}: {response.text}"
        ) from error

    result = response.json()

    try:
        parts = result["candidates"][0]["content"]["parts"]
    except (KeyError, IndexError, TypeError) as error:
        raise RuntimeError("Gemini returned no text response") from error

    text = "\n".join(part["text"] for part in parts if "text" in part)
    if not text:
        raise RuntimeError("Gemini returned no text response")
    return text


if __name__ == "__main__":
    user_prompt = input("Enter a prompt for Gemini: ")
    print(ask_gemini(user_prompt))
