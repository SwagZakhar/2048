from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QKeyEvent

class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("2048 на PyQt6")
        self.setFixedSize(400, 450)
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(10)
        
        self.labels = [[None] * self.game.size for _ in range(self.game.size)]
        
        for r in range(self.game.size):
            for c in range(self.game.size):
                label = QLabel("", self)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
                label.setStyleSheet(
                    "background-color: #CDC1B4; "
                    "color: #776E65; "
                    "border-radius: 5px;"
                )
                self.grid_layout.addWidget(label, r, c)
                self.labels[r][c] = label
                
        self.update_ui()

    def update_ui(self):
        """Обновляет текст на плитках."""
        for r in range(self.game.size):
            for c in range(self.game.size):
                value = self.game.grid[r][c]
                if value == 0:
                    self.labels[r][c].setText("")
                    self.labels[r][c].setStyleSheet("background-color: #CDC1B4; border-radius: 5px;")
                else:
                    self.labels[r][c].setText(str(value))
                    self.labels[r][c].setStyleSheet(
                        "background-color: #EEE4DA; color: #776E65; border-radius: 5px;"
                    )
        
        self.setWindowTitle(f"2048 | Счет: {self.game.score}")

    def keyPressEvent(self, event: QKeyEvent):
        """Обработка нажатия стрелки Влево."""
        if event.key() == Qt.Key.Key_Left:
            if self.game.move_left():
                self.game.add_new_tile()
                self.update_ui()
        else:
            super().keyPressEvent(event)