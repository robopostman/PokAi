# PokAi

## API client setup

The project includes a small JSON REST client. Configure the base URL and, if
needed, a bearer token in a local `.env` file:

1. Install dependencies: `python -m pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and set `API_BASE_URL` and `API_KEY`.
3. Use the client from your Python code:

```python
from api_client import APIClient

client = APIClient.from_env()
data = client.get("v1/status", params={"verbose": True})
print(data)
```

Use `client.post("v1/items", json={"name": "example"})` to send a JSON body.
Set `API_KEY` only when the API uses bearer-token authentication. HTTP errors,
connection errors, and invalid JSON responses are raised by the client
dependencies rather than being silently ignored.

## Send a prompt to Gemini

Set `GEMINI_API_KEY` in your local `.env` file. Optionally set `GEMINI_MODEL`
to choose another Gemini model; the default is `gemini-3.6-flash`. Then run:

```powershell
.\.venv\Scripts\python.exe ask_gemini.py
```

Enter a prompt when asked. You can also call `ask_gemini(prompt)` from another
Python file:

```python
from ask_gemini import ask_gemini

print(ask_gemini("Explain how Pokémon type matchups work."))
```

## Get help from a Pokémon

Run the task helper to enter a task, get a random Pokémon and its moves, and
ask Gemini how those moves might help. The response includes a harmless,
cartoon-style mishap:

```powershell
.\.venv\Scripts\python.exe pokemon_task_helper.py
```

For a graphical interface to enter the task and display the advice, run:

```powershell
.\.venv\Scripts\python.exe task_ui.py
```

The interface uses CustomTkinter, included in `requirements.txt`. It displays
the selected Pokémon's front sprite alongside the advice and reuses the same
Pokémon and Gemini configuration as the command-line helper.
