from __future__ import annotations

from io import BytesIO
from queue import Empty, Queue
from threading import Thread

import customtkinter as ctk
import requests
from PIL import Image

from pokemon_task_helper import get_pokemon_task_result


class PokemonTaskApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Pokémon Task Helper")
        self.geometry("720x640")
        self.minsize(520, 480)

        self._results: Queue[
            tuple[bool, str, Image.Image | None, str | None]
        ] = Queue()
        self._pokemon_image: ctk.CTkImage | None = None

        self.grid_columnconfigure(0, weight=1)

        heading = ctk.CTkLabel(
            self,
            text="What are you trying to do?",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        heading.grid(row=0, column=0, padx=24, pady=(24, 8), sticky="w")

        self.task_input = ctk.CTkTextbox(self, height=120, wrap="word")
        self.task_input.grid(row=1, column=0, padx=24, pady=(0, 12), sticky="ew")

        self.submit_button = ctk.CTkButton(
            self, text="Get Pokémon advice", command=self._submit_task
        )
        self.submit_button.grid(row=2, column=0, padx=24, pady=(0, 12), sticky="w")

        self.status_label = ctk.CTkLabel(self, text="", anchor="w", justify="left")
        self.status_label.grid(
            row=3, column=0, padx=24, pady=(0, 8), sticky="new"
        )

        self.sprite_label = ctk.CTkLabel(self, text="")
        self.sprite_label.grid(row=4, column=0, padx=24, pady=(0, 8), sticky="w")

        self.result = ctk.CTkTextbox(self, wrap="word")
        self.result.grid(row=5, column=0, padx=24, pady=(0, 24), sticky="nsew")
        self.grid_rowconfigure(5, weight=1)
        self.result.insert("1.0", "Your results will appear here.")
        self.result.configure(state="disabled")

    def _submit_task(self) -> None:
        task = self.task_input.get("1.0", "end").strip()
        if not task:
            self.status_label.configure(text="Please enter a task.")
            return

        self.submit_button.configure(state="disabled")
        self.status_label.configure(text="Getting advice... This may take a moment.")
        self.sprite_label.configure(image=None, text="")
        self._pokemon_image = None
        self._set_result("")
        Thread(target=self._get_advice, args=(task,), daemon=True).start()
        self.after(100, self._check_results)

    def _get_advice(self, task: str) -> None:
        try:
            advice, pokemon = get_pokemon_task_result(task)
            sprite = None
            sprite_error = None
            if pokemon.sprite_url:
                try:
                    response = requests.get(pokemon.sprite_url, timeout=15)
                    response.raise_for_status()
                    sprite = Image.open(BytesIO(response.content)).convert("RGBA")
                except (requests.RequestException, OSError) as error:
                    sprite_error = f"Could not load Pokémon image: {error}"
            self._results.put((True, advice, sprite, sprite_error))
        except Exception as error:
            self._results.put((False, str(error) or type(error).__name__, None, None))

    def _check_results(self) -> None:
        try:
            succeeded, message, sprite, sprite_error = self._results.get_nowait()
        except Empty:
            self.after(100, self._check_results)
            return

        self.submit_button.configure(state="normal")
        if succeeded:
            status = "Here’s your Pokémon advice:"
            if sprite is not None:
                self._pokemon_image = ctk.CTkImage(
                    light_image=sprite,
                    dark_image=sprite,
                    size=(160, 160),
                )
                self.sprite_label.configure(image=self._pokemon_image)
            elif sprite_error:
                status = f"{status} {sprite_error}"
            else:
                status = f"{status} No image is available for this Pokémon."
            self.status_label.configure(text=status)
            self._set_result(message)
        else:
            self.status_label.configure(text=f"Could not get advice: {message}")

    def _set_result(self, text: str) -> None:
        self.result.configure(state="normal")
        self.result.delete("1.0", "end")
        self.result.insert("1.0", text)
        self.result.configure(state="disabled")


def main() -> None:
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    app = PokemonTaskApp()
    app.mainloop()


if __name__ == "__main__":
    main()
