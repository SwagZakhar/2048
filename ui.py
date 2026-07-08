import os
from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QVBoxLayout, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent

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
}

HIGHSCORE_FILE = "highscore.txt"


class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("2048 на PyQt6")
        self.setFixedSize(400, 500)

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

        self.update_ui()

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

    def update_ui(self):
        for r in range(self.game.size):
            for c in range(self.game.size):
                value = self.game.grid[r][c]
                bg_color, text_color = TILE_COLORS.get(value, ("#3C3A32", "#F9F6F2"))
                if value == 0:
                    self.labels[r][c].setText("")
                else:
                    self.labels[r][c].setText(str(value))
                self.labels[r][c].setStyleSheet(
                    f"background-color: {bg_color}; color: {text_color}; border-radius: 5px;"
                )

        highscore = self.get_highscore()
        self.score_label.setText(f"Счёт: {self.game.score}  |  Рекорд: {max(highscore, self.game.score)}")

    def show_game_over_message(self):
        current_score = self.game.score
        old_highscore = self.get_highscore()
        is_new_record = current_score > old_highscore

        if is_new_record:
            self.save_highscore(current_score)
            title = "🎉 Новый рекорд!"
            message = f"Поздравляем! Вы побили прошлый рекорд!\n\nВаш счёт: {current_score}\nПредыдущий рекорд: {old_highscore}"
        else:
            title = "Игра окончена"
            message = f"Ходов больше нет.\n\nВаш счёт: {current_score}\nЛучший результат: {old_highscore}"

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        # Настройка кнопок на русском
        retry_button = msg_box.addButton("Заново", QMessageBox.ButtonRole.AcceptRole)
        exit_button = msg_box.addButton("Выход", QMessageBox.ButtonRole.RejectRole)
        
        msg_box.exec()

        if msg_box.clickedButton() == retry_button:
            self.game.reset_game()
            self.update_ui()
        else:
            self.close()

    def keyPressEvent(self, event: QKeyEvent):
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
            
            # Проверяем проигрыш после каждого успешного хода
            if self.game.is_game_over():
                self.show_game_over_message()