import unittest
from unittest.mock import Mock, patch

from get_pokemon import PokemonDetails, random_pokemon
from pokemon_task_helper import get_pokemon_task_advice, get_pokemon_task_result


class RandomPokemonTests(unittest.TestCase):
    @patch("get_pokemon.APIClient.from_env")
    @patch("get_pokemon.random.randint", return_value=25)
    def test_returns_pokemon_moves_and_front_default_sprite(
        self, _randint: Mock, from_env: Mock
    ) -> None:
        client = Mock()
        client.get.return_value = {
            "name": "pikachu",
            "moves": [{"move": {"name": "thunderbolt"}}],
            "sprites": {"front_default": "https://example.com/pikachu.png"},
        }
        from_env.return_value = client

        result = random_pokemon()

        self.assertEqual(
            result,
            PokemonDetails(
                name="pikachu",
                moves=["thunderbolt"],
                sprite_url="https://example.com/pikachu.png",
            ),
        )
        self.assertEqual(
            str(result), "Pokemon: pikachu\nMoves:\n- thunderbolt"
        )
        client.get.assert_called_once_with("pokemon/25")


class PokemonTaskHelperTests(unittest.TestCase):
    @patch("pokemon_task_helper.ask_gemini", return_value="Helpful advice")
    @patch("pokemon_task_helper.random_pokemon")
    def test_result_includes_advice_and_selected_pokemon(
        self, random_pokemon_mock: Mock, _ask_gemini_mock: Mock
    ) -> None:
        pokemon = PokemonDetails(
            name="pikachu",
            moves=["thunderbolt"],
            sprite_url="https://example.com/pikachu.png",
        )
        random_pokemon_mock.return_value = pokemon

        result = get_pokemon_task_result("Clean my room")

        self.assertEqual(result, ("Helpful advice", pokemon))

    @patch("pokemon_task_helper.get_pokemon_task_result")
    def test_advice_function_keeps_returning_text(
        self, result_mock: Mock
    ) -> None:
        result_mock.return_value = (
            "Helpful advice",
            PokemonDetails(name="pikachu", moves=[], sprite_url=None),
        )

        self.assertEqual(
            get_pokemon_task_advice("Clean my room"), "Helpful advice"
        )


if __name__ == "__main__":
    unittest.main()
