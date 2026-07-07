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

    def move_left(self):
        """Сдвигает элементы влево и сливает одинаковые плитки."""
        old_grid = [row[:] for row in self.grid]
        
        for r in range(self.size):
            # 1. Извлекаем только ненулевые элементы текущей строки
            non_zero = [num for num in self.grid[r] if num != 0]
            
            # 2. Сливаем одинаковые соседние числа
            new_row = []
            skip = False
            for i in range(len(non_zero)):
                if skip:
                    skip = False
                    continue
                # Если текущий элемент равен следующему — сливаем их
                if i + 1 < len(non_zero) and non_zero[i] == non_zero[i + 1]:
                    merged_value = non_zero[i] * 2
                    new_row.append(merged_value)
                    self.score += merged_value  # Начисляем очки за слияние
                    skip = True  # Следующий элемент мы уже учли, пропускаем его
                else:
                    new_row.append(non_zero[i])
            
            # 3. Дописываем нули до конца строки (до размера self.size)
            while len(new_row) < self.size:
                new_row.append(0)
                
            self.grid[r] = new_row
            
        # Возвращаем True, если матрица изменилась
        return self.grid != old_grid