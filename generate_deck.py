import json
from pathlib import Path


CARDS_FOLDER = Path("assets/cards")
OUTPUT_FILE = Path("data/decks/tarot_deck.json")

SUITS = {
    "major": None,
    "pentacles": "pentacles",
    "swords": "swords",
    "wands": "wands",
    "cups": "cups",
}

VALID_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def make_card_name(filename):
    # 01_ace_of_cups -> Ace Of Cups
    parts = filename.split("_")

    # Quita el número inicial
    if parts[0].isdigit():
        parts = parts[1:]

    return " ".join(parts).title()


def generate_deck():
    deck = []

    for folder_name, suit in SUITS.items():
        folder = CARDS_FOLDER / folder_name

        if not folder.exists():
            print(f"No encontré la carpeta: {folder}")
            continue

        files = sorted(
            file
            for file in folder.iterdir()
            if file.suffix.lower() in VALID_EXTENSIONS
        )

        for file in files:
            card = {
                "id": len(deck),
                "name": make_card_name(file.stem),
                "arcana": "major" if folder_name == "major" else "minor",
                "suit": suit,
                "image": file.as_posix(),
            }

            deck.append(card)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as json_file:
        json.dump(deck, json_file, ensure_ascii=False, indent=4)

    print(f"Mazo generado correctamente: {len(deck)} cartas")
    print(f"Archivo creado: {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_deck()