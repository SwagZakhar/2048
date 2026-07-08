import random

class Game2048:
    def __init__(self, size=4):
        self.size = size
        self.grid = []
        self.score = 0
        self.reset_game()

    def reset_game(self):
        self.grid = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [
            (r, c) for r in range(self.size) for c in range(self.size) if self.grid[r][c] == 0
        ]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def _slide_and_merge_row(self, row):
        non_zero = [num for num in row if num != 0]
        new_row = []
        skip = False
        for i in range(len(non_zero)):
            if skip:
                skip = False
                continue
            if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                merged_value = non_zero[i] * 2
                new_row.append(merged_value)
                self.score += merged_value
                skip = True
            else:
                new_row.append(non_zero[i])
        
        while len(new_row) < self.size:
            new_row.append(0)
        return new_row

    def move(self, direction):
        old_grid = [row[:] for row in self.grid]

        if direction == 'left':
            for r in range(self.size):
                self.grid[r] = self._slide_and_merge_row(self.grid[r])
        elif direction == 'right':
            for r in range(self.size):
                self.grid[r] = self._slide_and_merge_row(self.grid[r][::-1])[::-1]
        elif direction == 'up':
            for c in range(self.size):
                row = [self.grid[r][c] for r in range(self.size)]
                merged = self._slide_and_merge_row(row)
                for r in range(self.size):
                    self.grid[r][c] = merged[r]
        elif direction == 'down':
            for c in range(self.size):
                row = [self.grid[r][c] for r in range(self.size)][::-1]
                merged = self._slide_and_merge_row(row)[::-1]
                for r in range(self.size):
                    self.grid[r][c] = merged[r]

        return self.grid != old_grid

    def is_won(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] >= 4096:
                    return True
        return False

    def is_game_over(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return False

        for r in range(self.size):
            for c in range(self.size - 1):
                if self.grid[r][c] == self.grid[r][c + 1]:
                    return False

        for r in range(self.size - 1):
            for c in range(self.size):
                if self.grid[r][c] == self.grid[r + 1][c]:
                    return False

        return True