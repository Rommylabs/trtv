from PySide6.QtCore import Qt
from data.services import SERVICES
from models.deck import Deck
from ui.card_widget import DeckSpreadWidget
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QFrame,
    QMainWindow,
    QStackedWidget,

)


class ReadingOption(QFrame):
    def __init__(self, title, description, price, callback):
        super().__init__()

        self.setFixedSize(260, 280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(22, 22, 22, 22)
        layout.setSpacing(14)

        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 21px;
                font-weight: bold;
            }
        """)

        description_label = QLabel(description)
        description_label.setWordWrap(True)
        description_label.setAlignment(Qt.AlignCenter)
        description_label.setStyleSheet("""
            QLabel {
                color: #d7cedd;
                font-size: 14px;
            }
        """)

        price_label = QLabel(price)
        price_label.setAlignment(Qt.AlignCenter)
        price_label.setStyleSheet("""
            QLabel {
                color: #e1bc68;
                font-size: 20px;
                font-weight: bold;
            }
        """)

        button = QPushButton("Elegir")
        button.clicked.connect(callback)
        button.setStyleSheet("""
            QPushButton {
                background-color: #6e3f87;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-size: 15px;
            }

            QPushButton:hover {
                background-color: #8750a3;
            }
        """)

        layout.addWidget(title_label)
        layout.addWidget(description_label)
        layout.addStretch()
        layout.addWidget(price_label)
        layout.addWidget(button)

        self.setStyleSheet("""
            ReadingOption {
                background-color: #211829;
                border: 1px solid #76518b;
                border-radius: 18px;
            }
        """)


class ProductScreen(QWidget):
    def __init__(self, selection_callback):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(30)

        title = QLabel("Elige tu lectura")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 34px;
                font-weight: bold;
            }
        """)

        subtitle = QLabel(
            "Selecciona el tipo de lectura que quieres realizar."
        )
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: #cfc6d5;
                font-size: 16px;
            }
        """)

        options = QHBoxLayout()
        options.setSpacing(25)
        options.setAlignment(Qt.AlignCenter)

        one_card = ReadingOption(
            "Consejo del día",
            "Una carta para recibir orientación y energía para tu día.",
            "$ —",
            lambda: selection_callback("daily_advice"),
        )

        three_cards = ReadingOption(
            "Tres cartas",
            "Una lectura con mayor contexto, evolución y orientación.",
            "$ —",
            lambda: selection_callback("full_reading"),
        )

        deep_reading = ReadingOption(
            "Lectura profunda",
            "Una interpretación más extensa para situaciones complejas.",
            "Próximamente",
            lambda: None,
        )

        options.addWidget(one_card)
        options.addWidget(three_cards)
        options.addWidget(deep_reading)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addStretch()
        layout.addLayout(options)
        layout.addStretch()

        self.setStyleSheet("""
            ProductScreen {
                background-color: #17131f;
            }
        """)


class IntroScreen(QWidget):
    def __init__(self, start_callback):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("TAROTVIA")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 44px;
                font-weight: bold;
            }
        """)

        subtitle = QLabel("Lecturas de tarot")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet("""
            QLabel {
                color: #cfcfcf;
                font-size: 18px;
            }
        """)

        button = QPushButton("Comenzar lectura")
        button.setFixedWidth(220)
        button.setStyleSheet("""
            QPushButton {
                background-color: #6e3f87;
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #8750a3;
            }
        """)
        button.clicked.connect(start_callback)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(20)
        layout.addWidget(button, alignment=Qt.AlignCenter)

        self.setStyleSheet("""
            QWidget {
                background-color: #17131f;
            }
        """)


class CardPlaceholder(QFrame):
    def __init__(self, text):
        super().__init__()

        self.setFixedSize(140, 220)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel(text)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("""
            QLabel {
                color: #fff7ea;
                font-size: 16px;
                font-weight: bold;
            }
        """)

        layout.addWidget(label)

        self.setStyleSheet("""
            QFrame {
                background-color: rgba(255, 248, 235, 0.08);
                border: 2px dashed #f2d18b;
                border-radius: 14px;
            }
        """)


class TableScreen(QWidget):
    def __init__(self, service=None):
        super().__init__()
        self.service = service

        outer_layout = QVBoxLayout(self)
        outer_layout.setAlignment(Qt.AlignCenter)
        outer_layout.setContentsMargins(40, 30, 40, 30)

        title = QLabel("Mesa de lectura")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                color: #f8e7d0;
                font-size: 28px;
                font-weight: bold;
                margin-bottom: 10px;
            }
        """)

        cloth = QFrame()
        cloth.setMinimumSize(950, 470)
        cloth.setStyleSheet("""
            QFrame {
                background-color: #8f1028;
                border: 4px solid #d4af37;
                border-radius: 26px;
            }
        """)

        cloth_layout = QVBoxLayout(cloth)
        cloth_layout.setContentsMargins(28, 24, 28, 24)
        cloth_layout.setSpacing(18)

        top_ornament = QLabel("❦   ♘   ❦   ♘   ❦")
        top_ornament.setAlignment(Qt.AlignCenter)
        top_ornament.setStyleSheet("""
            QLabel {
                color: #fff4de;
                font-size: 22px;
                font-weight: bold;
            }
        """)

        middle_band = QLabel("✦  UNICORNIOS DORADOS  ✦")
        middle_band.setAlignment(Qt.AlignCenter)
        middle_band.setStyleSheet("""
            QLabel {
                color: #fff4de;
                background-color: rgba(255, 255, 255, 0.10);
                border: 2px solid #f3e5c5;
                border-radius: 12px;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
            }
        """)

        cards_row = QHBoxLayout()
        cards_row.setSpacing(35)
        cards_row.setAlignment(Qt.AlignCenter)

        cards_count = 3

        if self.service is not None:
            cards_count = self.service["cards"]
            
        deck_name = self.service["deck"]

        deck = Deck(
            deck_name,
            f"assets/cards/{deck_name}"
        )

        deck.load_major_arcana()
        cards = deck.cards

        back_path = f"assets/cards/{deck_name}/back.jpg"

        spread = DeckSpreadWidget(
        cards,
        back_path,
        cards_per_row=11,
        max_selections=cards_count,
        )

        cards_row.addWidget(spread)

        bottom_ornament = QLabel("❦   ♘   ❦   ♘   ❦")
        bottom_ornament.setAlignment(Qt.AlignCenter)
        bottom_ornament.setStyleSheet("""
            QLabel {
                color: #fff4de;
                font-size: 22px;
                font-weight: bold;
            }
        """)

        hint = QLabel("Selecciona tus cartas para comenzar la tirada")
        hint.setAlignment(Qt.AlignCenter)
        hint.setStyleSheet("""
            QLabel {
                color: #ffe9c8;
                font-size: 15px;
                margin-top: 6px;
            }
        """)

        cloth_layout.addWidget(top_ornament)
        cloth_layout.addWidget(middle_band)
        cloth_layout.addStretch()
        cloth_layout.addLayout(cards_row)
        cloth_layout.addWidget(hint)
        cloth_layout.addStretch()
        cloth_layout.addWidget(bottom_ornament)

        outer_layout.addWidget(title)
        outer_layout.addWidget(cloth)

        self.setStyleSheet("""
            QWidget {
                background-color: #17131f;
            }
        """)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Tarotvia")
        self.resize(1200, 750)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        self.intro_screen = IntroScreen(self.show_product_screen)
        self.product_screen = ProductScreen(self.select_product)
        self.table_screen = None

        self.stack.addWidget(self.intro_screen)
        self.stack.addWidget(self.product_screen)

    def show_table_screen(self):
        self.stack.setCurrentWidget(self.table_screen)

    def show_product_screen(self):
        self.stack.setCurrentWidget(self.product_screen)

    def select_product(self, product):
        self.selected_product = product
        self.selected_service = SERVICES[product]

        print("Servicio elegido:", product)
        print("Configuración:", self.selected_service)

        if self.table_screen is not None:
            self.stack.removeWidget(self.table_screen)
            self.table_screen.deleteLater()

        self.table_screen = TableScreen(self.selected_service)
        self.stack.addWidget(self.table_screen)
        self.stack.setCurrentWidget(self.table_screen)