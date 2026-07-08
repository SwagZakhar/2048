import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QGridLayout, QLabel, QVBoxLayout,
    QHBoxLayout, QPushButton, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent, QColor

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
    4096: ("#A370F7", "#F9F6F2"),  # Цвет для победной плитки
}

HIGHSCORE_FILE = "highscore.txt"


class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("2048 game")
        self.setFixedSize(400, 500)
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)

        self.score_label = QLabel("Счёт: 0", self)
        self.score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.score_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.score_label.setStyleSheet("color: #776E65; padding: 10px;")
        main_layout.addWidget(self.score_label)

        grid_widget = QWidget(self)
        self.grid_layout = QGridLayout(grid_widget)
        self.grid_layout.setSpacing(10)
        main_layout.addWidget(grid_widget)

        self.labels = [[None] * self.game.size for _ in range(self.game.size)]

        for r in range(self.game.size):
            for c in range(self.game.size):
                label = QLabel("", self)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
                self.grid_layout.addWidget(label, r, c)
                self.labels[r][c] = label

        self.init_game_over_overlay()
        self.update_ui()

    def init_game_over_overlay(self):
        self.overlay = QWidget(self.central_widget)
        self.overlay.setGeometry(0, 0, 400, 500)
        self.overlay.setStyleSheet("background-color: rgba(238, 228, 218, 200);")
        self.overlay.hide()

        outer_layout = QVBoxLayout(self.overlay)
        outer_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.overlay_card = QWidget(self.overlay)
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

        exit_button = QPushButton("Выход", self.overlay_card)
        exit_button.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        exit_button.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_button.setStyleSheet(
            "QPushButton { background-color: #BBADA0; color: #F9F6F2; padding: 10px 0px; border-radius: 8px; border: none; }"
            "QPushButton:hover { background-color: #A69787; }"
        )
        exit_button.clicked.connect(self.close)
        buttons_layout.addWidget(exit_button)

        card_layout.addLayout(buttons_layout)

        reset_highscore_button = QPushButton("Сбросить рекорд", self.overlay_card)
        reset_highscore_button.setFont(QFont("Arial", 10))
        reset_highscore_button.setCursor(Qt.CursorShape.PointingHandCursor)
        reset_highscore_button.setStyleSheet(
            "QPushButton { background-color: transparent; color: #8F7A66; text-decoration: underline; border: none; padding: 4px; }"
            "QPushButton:hover { color: #776E65; }"
        )
        reset_highscore_button.clicked.connect(self.reset_highscore)
        card_layout.addWidget(reset_highscore_button, alignment=Qt.AlignmentFlag.AlignCenter)

        outer_layout.addWidget(self.overlay_card)

    def get_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            try:
                with open(HIGHSCORE_FILE, "r") as f:
                    return int(f.read().strip())
            except ValueError:
                return 0
        return 0

    def save_highscore(self, score):
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(score))

    def reset_highscore(self):
        if os.path.exists(HIGHSCORE_FILE):
            os.remove(HIGHSCORE_FILE)
        self.update_ui()

    def update_ui(self):
        for r in range(self.game.size):
            for c in range(self.game.size):
                value = self.game.grid[r][c]
                bg_color, text_color = TILE_COLORS.get(value, ("#3C3A32", "#F9F6F2"))
                
                label = self.labels[r][c]
                if value == 0:
                    label.setText("")
                else:
                    label.setText(str(value))
                
                if value >= 1000:
                    font_size = 18
                else:
                    font_size = 22
                
                label.setFont(QFont("Arial", font_size, QFont.Weight.Bold))
                label.setStyleSheet(
                    f"background-color: {bg_color}; color: {text_color}; border-radius: 5px;"
                )

        highscore = self.get_highscore()
        self.score_label.setText(f"Счёт: {self.game.score}  |  Рекорд: {max(highscore, self.game.score)}")

    def show_game_over_message(self, won=False):
        current_score = self.game.score
        old_highscore = self.get_highscore()
        
        if current_score > old_highscore:
            self.save_highscore(current_score)

        if won:
            self.overlay_icon.setText("👑")
            self.overlay_title.setText("Вы победили!")
            self.overlay_message.setText(
                f"Поздравляем! Вы успешно объединили две плитки 2048 и получили 4096!\nВаш счёт: {current_score}"
            )
        elif current_score > old_highscore:
            self.overlay_icon.setText("🏆")
            self.overlay_title.setText("Новый рекорд!")
            self.overlay_message.setText(
                f"Поздравляем! Вы побили прошлый рекорд!\nВаш счёт: {current_score}\nПредыдущий рекорд: {old_highscore}"
            )
        else:
            self.overlay_icon.setText("😕")
            self.overlay_title.setText("Игра окончена")
            self.overlay_message.setText(
                f"Ходов больше нет.\nВаш счёт: {current_score}\nЛучший результат: {old_highscore}"
            )

        self.overlay.raise_()
        self.overlay.show()

    def restart_game(self):
        self.game.reset_game()
        self.overlay.hide()
        self.update_ui()
        self.setFocus()

    def keyPressEvent(self, event: QKeyEvent):
        if self.overlay.isVisible():
            return

        moved = False
        if event.key() == Qt.Key.Key_Left:
            moved = self.game.move('left')
        elif event.key() == Qt.Key.Key_Right:
            moved = self.game.move('right')
        elif event.key() == Qt.Key.Key_Up:
            moved = self.game.move('up')
        elif event.key() == Qt.Key.Key_Down:
            moved = self.game.move('down')
        else:
            super().keyPressEvent(event)
            return

        if moved:
            self.game.add_new_tile()
            self.update_ui()

            if self.game.is_won():
                self.show_game_over_message(won=True)
            elif self.game.is_game_over():
                self.show_game_over_message(won=False)