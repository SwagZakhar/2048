from PyQt6.QtWidgets import QMainWindow, QWidget, QGridLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class GameWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("2048 на PyQt6")
        self.setFixedSize(400, 450)  # Окно фиксированного размера
        
        # Главный виджет и сетка
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.grid_layout = QGridLayout(self.central_widget)
        self.grid_layout.setSpacing(10)  # Отступы между плитками
        
        # Двумерный массив для хранения графических ярлыков (label)
        self.labels = [[None] * self.game.size for _ in range(self.game.size)]
        
        # Создаем сетку из QLabel
        for r in range(self.game.size):
            for c in range(self.game.size):
                label = QLabel("", self)
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setFont(QFont("Arial", 22, QFont.Weight.Bold))
                
                # Задаем базовый стиль (позже сделаем красивые цвета для каждого числа)
                label.setStyleSheet(
                    "background-color: #CDC1B4; "
                    "color: #776E65; "
                    "border-radius: 5px;"
                )
                
                self.grid_layout.addWidget(label, r, c)
                self.labels[r][c] = label
                
        self.update_ui()

    def update_ui(self):
        """Обновляет текст на плитках в соответствии с матрицей логики."""
        for r in range(self.game.size):
            for c in range(self.game.size):
                value = self.game.grid[r][c]
                if value == 0:
                    self.labels[r][c].setText("")
                    self.labels[r][c].setStyleSheet("background-color: #CDC1B4; border-radius: 5px;")
                else:
                    self.labels[r][c].setText(str(value))
                    # Временный простой стиль для цифр
                    self.labels[r][c].setStyleSheet(
                        f"background-color: #EEE4DA; color: #776E65; border-radius: 5px;"
                    )
        
        # Выводим счет в заголовок окна (пока не создали отдельное поле для счета)
        self.setWindowTitle(f"2048 | Счет: {self.game.score}")