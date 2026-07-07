import sys
from PyQt6.QtWidgets import QApplication
from logic import Game2048
from ui import GameWindow

def main():
    app = QApplication(sys.argv)
    game = Game2048()
    window = GameWindow(game)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()