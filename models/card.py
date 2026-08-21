class Card:
    def __init__(self, card_id, name, number, image_path, deck_name):
        self.card_id = card_id
        self.name = name
        self.number = number
        self.image_path = image_path
        self.deck_name = deck_name

    def __repr__(self):
        return f"Card({self.deck_name}: {self.number} - {self.name})"