from pathlib import Path

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QFrame
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

class CardBackWidget(QFrame):
    clicked = Signal(object)

    def __init__(self, card, back_path):
        super().__init__()

        self.card = card
        self.back_path = Path(back_path)
        
        self.base_x = 0
        self.base_y = 0
        self.is_hovered = False

        self.setFixedSize(120, 190)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setAttribute(Qt.WA_TransparentForMouseEvents, True)

        pixmap = QPixmap(str(self.back_path))

        if not pixmap.isNull():
            pixmap = pixmap.scaled(
                120,
                190,
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation,
            )
            self.image_label.setPixmap(pixmap)
        else:
            self.image_label.setText("Carta")
            self.image_label.setStyleSheet("color: white;")

        layout.addWidget(self.image_label)

        self.setStyleSheet("""
            QFrame {
                background: transparent;
                border: none;
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.card)

        super().mousePressEvent(event)
    
    def set_base_position(self, x, y):
        self.base_x = x
        self.base_y = y
        self.move(x, y)


    def enterEvent(self, event):
        if not self.is_hovered:
            self.is_hovered = True
            self.raise_()
            self.move(self.base_x, self.base_y - 18)

        super().enterEvent(event)


    def leaveEvent(self, event):
        self.is_hovered = False
        self.move(self.base_x, self.base_y)

        parent = self.parent()
        if parent and hasattr(parent, "restore_card_order"):
            parent.restore_card_order()

        super().leaveEvent(event)

class DeckSpreadWidget(QWidget):
    card_selected = Signal(object)

    def __init__(self, cards, back_path, cards_per_row=13, max_selections=1):
        super().__init__()

        self.cards = cards
        self.back_path = back_path
        self.cards_per_row = cards_per_row
        self.card_widgets = []
        self.selected_cards = []
        self.max_selections = max_selections

        self.card_width = 120
        self.card_height = 190

        # Cuánto se ve de cada carta antes de la siguiente.
        self.horizontal_step = 42

        # Espacio vertical entre filas.
        self.vertical_step = 145

        self.build_spread()

    def build_spread(self):
        total_cards = len(self.cards)

        for index, card in enumerate(self.cards):
            row = index // self.cards_per_row
            column = index % self.cards_per_row

            card_widget = CardBackWidget(
                card,
                self.back_path
            )

            card_widget.clicked.connect(self.on_card_clicked)

            x = column * self.horizontal_step
            y = row * self.vertical_step

            card_widget.setParent(self)
            card_widget.set_base_position(x, y)

            self.card_widgets.append(card_widget)

        rows = (total_cards + self.cards_per_row - 1) // self.cards_per_row

        spread_width = (
            (min(total_cards, self.cards_per_row) - 1)
            * self.horizontal_step
            + self.card_width
        )

        spread_height = (
            (rows - 1)
            * self.vertical_step
            + self.card_height
        )

        self.setFixedSize(spread_width, spread_height)

    def on_card_clicked(self, card):
        if card in self.selected_cards:
            return

        if len(self.selected_cards) >= self.max_selections:
            return

        self.selected_cards.append(card)

        print("Carta seleccionada:", card)
        print(
            f"Selecciones: {len(self.selected_cards)} / {self.max_selections}"
        )

        self.card_selected.emit(card)
        
    def restore_card_order(self):
        for card_widget in self.card_widgets:
            card_widget.raise_()