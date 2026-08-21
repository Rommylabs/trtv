from models.deck import Deck

deck = Deck(
    "visconti_sforza",
    "assets/cards/visconti_sforza"
)

cards = deck.load_major_arcana()

print("Cartas cargadas:", len(cards))
print("Primera carta:", cards[0] if cards else "ninguna")
print("Carta elegida:", deck.draw(1))