import random

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.grid = []
        self.score = 0
        self.reset_game()

    def reset_game(self):
        """Сбрасывает игру и создает пустое поле с двумя плитками."""
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        """Находит случайную пустую ячейку и ставит туда 2 (90%) или 4 (10%)."""
        empty_cells = [
            (r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0
        ]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2