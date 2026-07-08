from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel, QVBoxLayout
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

        self.score_label.setText(f"Счёт: {self.game.score}")

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