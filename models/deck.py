from pathlib import Path
import random

from models.card import Card


class Deck:
    def __init__(self, deck_name, base_path):
        self.deck_name = deck_name
        self.base_path = Path(base_path)
        self.cards = []

    def load_major_arcana(self):
        major_path = self.base_path / "major"

        if not major_path.exists():
            raise FileNotFoundError(
                f"No existe la carpeta de arcanos mayores: {major_path}"
            )

        self.cards = []

        for image_file in sorted(major_path.iterdir()):
            if image_file.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp"}:
                continue

            stem = image_file.stem

            try:
                number_text, card_id = stem.split("_", 1)
                number = int(number_text)
            except ValueError:
                print(f"Archivo ignorado por nombre inválido: {image_file.name}")
                continue

            name = card_id.replace("_", " ").title()

            card = Card(
                card_id=card_id,
                name=name,
                number=number,
                image_path=str(image_file),
                deck_name=self.deck_name,
            )

            self.cards.append(card)

        return self.cards

    def draw(self, amount=1):
        if amount > len(self.cards):
            raise ValueError(
                f"Se pidieron {amount} cartas, pero el mazo tiene {len(self.cards)}."
            )

        return random.sample(self.cards, amount)