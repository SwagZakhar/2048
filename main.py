import sys
from PyQt6.QtWidgets import QApplication
from logic import Game2048
from ui import GameWindow

def main():
    # Создаем экземпляр приложения PyQt
    app = QApplication(sys.argv)
    
    # Инициализируем логику игры
    game = Game2048()
    
    # Инициализируем графическое окно и передаем туда логику
    window = GameWindow(game)
    window.show()
    
    # Запускаем главный цикл приложения
    sys.exit(app.exec())

if __name__ == "__main__":
    main()