import random
from dataclasses import dataclass

from api_client import APIClient


@dataclass(frozen=True)
class PokemonDetails:
    name: str
    moves: list[str]
    sprite_url: str | None

    def __str__(self) -> str:
        formatted_moves = "\n".join(f"- {move_name}" for move_name in self.moves)
        return f"Pokemon: {self.name}\nMoves:\n{formatted_moves}"


def random_pokemon() -> PokemonDetails:
    client = APIClient.from_env()
    pokemon_id = random.randint(1, 1025)
    pokemon = client.get(f"pokemon/{pokemon_id}")
    move_names = [entry["move"]["name"] for entry in pokemon["moves"]]
    return PokemonDetails(
        name=pokemon["name"],
        moves=move_names,
        sprite_url=pokemon["sprites"]["front_default"],
    )


if __name__ == "__main__":
    print(random_pokemon())
