import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent, QColor
from logic import Game2048

TILE_COLORS = {
    0: ("#CDC1B4", "#776E65"),
    2: ("#EEE4DA", "#776E65"),
    4: ("#EDE0C8", "#776E65"),
    8: ("#F2B179", "#F9F6F2"),
    16: ("#F59563", "#F9F6F2"),
    32: ("#F67C5F", "#F9F6F2"),
    64: ("#F65E3B", "#F9F6F2"),
    128: ("#EDCF72", "#F9F6F2"),
    256: ("#EDCC61", "#F9F6F2"),
    512: ("#EDC850", "#F9F6F2"),
    1024: ("#EDC53F", "#F9F6F2"),
    2048: ("#EDC22E", "#F9F6F2"),
    4096: ("#A370F7", "#F9F6F2"),
    8192: ("#8246E2", "#F9F6F2"),
    16384: ("#5E25B1", "#F9F6F2"),
    32768: ("#3F1480", "#F9F6F2"),
}

HIGHSCORE_FILE_TEMPLATE = "highscore_{}.txt"

GRID_AREA = 336
GRID_SPACING = 12
GRID_MARGIN = 12


class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.labels = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("2048 game")
        self.setFixedSize(400, 520)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setStyleSheet("background-color: #FAF8EF;")

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        top_bar_layout = QHBoxLayout()
        top_bar_layout.setSpacing(10)

        self.score_label = QLabel("Счёт: 0   |   Рекорд: 0", self)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.score_label.setStyleSheet("background-color: #BBADA0; color: #F9F6F2; border-radius: 6px; padding: 6px 4px;")
        top_bar_layout.addWidget(self.score_label, stretch=1)

        in_game_menu_button = QPushButton("Меню", self)
        in_game_menu_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        in_game_menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
        in_game_menu_button.setFixedWidth(80)
        in_game_menu_button.setStyleSheet(
            "QPushButton { background-color: #8F7A66; color: #F9F6F2; border-radius: 6px; padding: 8px; }"
            "QPushButton:hover { background-color: #7A6857; }"
        )
        in_game_menu_button.clicked.connect(self.show_size_menu)
        top_bar_layout.addWidget(in_game_menu_button)

        main_layout.addLayout(top_bar_layout)

        self.grid_widget = QWidget(self)
        self.grid_widget.setStyleSheet("background-color: #BBADA0; border-radius: 6px;")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(GRID_SPACING)
        self.grid_layout.setContentsMargins(GRID_MARGIN, GRID_MARGIN, GRID_MARGIN, GRID_MARGIN)
        main_layout.addWidget(self.grid_widget, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.build_grid_labels()

        self.init_game_over_overlay()
        self.init_size_menu_overlay()

        self.update_ui()
        self.show_size_menu()

    def build_grid_labels(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        n = self.game.size
        cell_size = (GRID_AREA - GRID_SPACING * (n - 1)) // n
        total_size = cell_size * n + GRID_SPACING * (n - 1) + GRID_MARGIN * 2
        self.grid_widget.setFixedSize(total_size, total_size)

        self.labels = [[None] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                label = QLabel("", self.grid_widget)
                label.setFixedSize(cell_size, cell_size)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.grid_layout.addWidget(label, r, c)
                self.labels[r][c] = label

    def tile_font_size(self, value):
        if self.game.size <= 4:
            base = 20
        elif self.game.size == 5:
            base = 16
        else:
            base = 13
            
        # Уменьшаем шрифт для больших чисел (пятизначных и более)
        if value >= 10000:
            return base - 6
        elif value >= 1000:
            return base - 4
        return base

    def init_size_menu_overlay(self):
        self.size_menu_overlay = QWidget(self.central_widget)
        self.size_menu_overlay.setGeometry(0, 0, 400, 520)
        self.size_menu_overlay.setStyleSheet("background-color: rgba(238, 228, 218, 220);")
        self.size_menu_overlay.hide()

        outer_layout = QVBoxLayout(self.size_menu_overlay)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QWidget(self.size_menu_overlay)
        card.setFixedWidth(300)
        card.setStyleSheet("background-color: #FAF8EF; border-radius: 16px;")

        shadow = QGraphicsDropShadowEffect(card)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 120))
        card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(12)

        title = QLabel("2048", card)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        title.setStyleSheet("color: #776E65;")
        card_layout.addWidget(title)

        subtitle = QLabel("Выберите размер поля", card)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setFont(QFont("Arial", 13))
        subtitle.setStyleSheet("color: #8F7A66;")
        card_layout.addWidget(subtitle)

        for size, label_text in ((4, "4 × 4"), (5, "5 × 5"), (6, "6 × 6")):
            btn = QPushButton(label_text, card)
            btn.setFont(QFont("Arial", 13, QFont.Weight.Bold))
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                "QPushButton { background-color: #8F7A66; color: #F9F6F2; padding: 10px 0px; border-radius: 8px; border: none; }"
                "QPushButton:hover { background-color: #7A6857; }"
            )
            btn.clicked.connect(lambda checked, s=size: self.start_new_game(s))
            card_layout.addWidget(btn)

        outer_layout.addWidget(card)

    def show_size_menu(self):
        self.game_over_overlay.hide()
        self.size_menu_overlay.raise_()
        self.size_menu_overlay.show()

    def start_new_game(self, size):
        self.game = Game2048(size=size)
        self.build_grid_labels()
        self.size_menu_overlay.hide()
        self.game_over_overlay.hide()
        self.update_ui()
        self.setFocus()

    def highscore_file(self):
        return HIGHSCORE_FILE_TEMPLATE.format(self.game.size)

    def get_highscore(self):
        path = self.highscore_file()
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    return int(f.read().strip())
            except Exception:
                return 0
        return 0

    def save_highscore(self, score):
        try:
            with open(self.highscore_file(), "w") as f:
                f.write(str(score))
        except Exception:
            pass

    def init_game_over_overlay(self):
        self.game_over_overlay = QWidget(self.central_widget)
        self.game_over_overlay.setGeometry(0, 0, 400, 520)
        self.game_over_overlay.setStyleSheet("background-color: rgba(238, 228, 218, 200);")
        self.game_over_overlay.hide()

        outer_layout = QVBoxLayout(self.game_over_overlay)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.overlay_card = QWidget(self.game_over_overlay)
        self.overlay_card.setFixedWidth(320)
        self.overlay_card.setStyleSheet("background-color: #FAF8EF; border-radius: 16px;")

        shadow = QGraphicsDropShadowEffect(self.overlay_card)
        shadow.setBlurRadius(30)
        shadow.setXOffset(0)
        shadow.setYOffset(6)
        shadow.setColor(QColor(0, 0, 0, 120))
        self.overlay_card.setGraphicsEffect(shadow)

        card_layout = QVBoxLayout(self.overlay_card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(12)

        self.overlay_icon = QLabel("", self.overlay_card)
        self.overlay_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overlay_icon.setFont(QFont("Arial", 32))
        card_layout.addWidget(self.overlay_icon)

        self.overlay_title = QLabel("Игра окончена", self.overlay_card)
        self.overlay_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overlay_title.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.overlay_title.setStyleSheet("color: #776E65;")
        self.overlay_title.setWordWrap(True)
        card_layout.addWidget(self.overlay_title)

        self.overlay_message = QLabel("", self.overlay_card)
        self.overlay_message.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.overlay_message.setFont(QFont("Arial", 12))
        self.overlay_message.setStyleSheet("color: #8F7A66;")
        self.overlay_message.setWordWrap(True)
        self.overlay_message.setMinimumHeight(90)
        card_layout.addWidget(self.overlay_message)

        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(12)

        retry_button = QPushButton("Заново", self.overlay_card)
        retry_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        retry_button.setCursor(Qt.CursorShape.PointingHandCursor)
        retry_button.setStyleSheet(
            "QPushButton { background-color: #8F7A66; color: #F9F6F2; padding: 10px 0px; border-radius: 8px; border: none; }"
            "QPushButton:hover { background-color: #7A6857; }"
        )
        retry_button.clicked.connect(self.restart_game)
        buttons_layout.addWidget(retry_button)

        menu_button = QPushButton("Меню", self.overlay_card)
        menu_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        menu_button.setCursor(Qt.CursorShape.PointingHandCursor)
        menu_button.setStyleSheet(
            "QPushButton { background-color: #BBADA0; color: #F9F6F2; padding: 10px 0px; border-radius: 8px; border: none; }"
            "QPushButton:hover { background-color: #A69787; }"
        )
        menu_button.clicked.connect(self.show_size_menu)
        buttons_layout.addWidget(menu_button)

        exit_button = QPushButton("Выход", self.overlay_card)
        exit_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        exit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_button.setStyleSheet(
            "QPushButton { background-color: #8F7A66; color: #F9F6F2; padding: 10px 0px; border-radius: 8px; border: none; }"
            "QPushButton:hover { background-color: #7A6857; }"
        )
        exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(exit_button)

        card_layout.addLayout(buttons_layout)

        outer_layout.addWidget(self.overlay_card)

    def update_ui(self):
        for r in range(self.game.size):
            for c in range(self.game.size):
                value = self.game.grid[r][c]
                bg_color, text_color = TILE_COLORS.get(value, ("#242119", "#F9F6F2"))

                label = self.labels[r][c]
                if value == 0:
                    label.setText("")
                else:
                    label.setText(str(value))

                label.setFont(QFont("Arial", self.tile_font_size(value), QFont.Weight.Bold))
                label.setStyleSheet(
                    f"background-color: {bg_color}; color: {text_color}; border-radius: 4px;"
                )

        old_highscore = self.get_highscore()
        if self.game.score > old_highscore:
            self.save_highscore(self.game.score)
            current_highscore = self.game.score
        else:
            current_highscore = old_highscore

        text_content = f"Счёт: {self.game.score}   |   Рекорд: {current_highscore}"
        
        if len(text_content) > 32:
            font_size = 12
        elif len(text_content) > 26:
            font_size = 14
        else:
            font_size = 16

        self.score_label.setFont(QFont("Arial", font_size, QFont.Weight.Bold))
        self.score_label.setText(text_content)

    def show_game_over_message(self, won=False):
        current_score = self.game.score
        old_highscore = self.get_highscore()

        if current_score >= old_highscore and current_score > 0:
            self.overlay_icon.setText("🏆")
            self.overlay_title.setText("Новый рекорд!")
            self.overlay_message.setText(
                f"Поздравляем! Вы побили прошлый рекорд!\nВаш счёт: {current_score}"
            )
        else:
            self.overlay_icon.setText("😕")
            self.overlay_title.setText("Игра окончена")
            self.overlay_message.setText(
                f"Ходов больше нет.\nВаш счёт: {current_score}\nЛучший результат: {old_highscore}"
            )

        self.game_over_overlay.raise_()
        self.game_over_overlay.show()

    def restart_game(self):
        self.game.reset_game()
        self.game_over_overlay.hide()
        self.update_ui()
        self.setFocus()

    def keyPressEvent(self, event: QKeyEvent):
        if self.game_over_overlay.isVisible() or self.size_menu_overlay.isVisible():
            return

        moved = False
        key = event.key()
        if key in (Qt.Key.Key_Left, Qt.Key.Key_A):
            moved = self.game.move('left')
        elif key in (Qt.Key.Key_Right, Qt.Key.Key_D):
            moved = self.game.move('right')
        elif key in (Qt.Key.Key_Up, Qt.Key.Key_W):
            moved = self.game.move('up')
        elif key in (Qt.Key.Key_Down, Qt.Key.Key_S):
            moved = self.game.move('down')
        else:
            super().keyPressEvent(event)
            return

        if moved:
            self.game.add_new_tile()
            self.update_ui()

            if self.game.is_game_over():
                self.show_game_over_message(won=False)