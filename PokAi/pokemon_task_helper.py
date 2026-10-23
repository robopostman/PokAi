from ask_gemini import ask_gemini
from get_pokemon import random_pokemon


def get_pokemon_task_advice(task: str) -> str:
    if not task.strip():
        raise ValueError("Task cannot be empty")

    pokemon_details = random_pokemon()
    prompt = (
        "A user wants help with this task:\n"
        f"{task}\n\n"
        "Here is a randomly selected Pokemon and its available moves:\n"
        f"{pokemon_details}\n\n"
        "Explain how this Pokemon could use its listed moves to help with the "
        "task. Keep the answer playful and include one funny, harmless, "
        "cartoon-style disastrous mishap. Keep the mishap fictional and "
        "non-violent, with no real-world danger or injury."
    )
    return ask_gemini(prompt)


def main() -> None:
    task = input("What task are you trying to perform? ").strip()
    if not task:
        raise SystemExit("Please enter a task.")

    print(get_pokemon_task_advice(task))


if __name__ == "__main__":
    main()
