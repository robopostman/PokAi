import random

from api_client import APIClient


def random_pokemon() -> str:
    client = APIClient.from_env()
    pokemon_id = random.randint(1, 1025)
    pokemon = client.get(f"pokemon/{pokemon_id}")
    pokemon_name = pokemon["name"]
    move_names = [entry["move"]["name"] for entry in pokemon["moves"]]
    formatted_moves = "\n".join(f"- {move_name}" for move_name in move_names)
    return f"Pokemon: {pokemon_name}\nMoves:\n{formatted_moves}"


if __name__ == "__main__":
    print(random_pokemon())
