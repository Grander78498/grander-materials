import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def rastrigin(x: np.ndarray):
    return np.sum(np.square(x) - 10 * np.cos(2 * np.pi * x) + 10, axis=-1)

class BeeColony:
    def __init__(self, bee_count: int = 100,
                       max_iter: int = 5,
                       max_distance: float = 1,
                       search_size: float = 1,
                       n: int = 2):
        self.bee_count = bee_count
        self.max_iter = max_iter
        self.max_distance = max_distance
        self.search_size = search_size
        self.n = n
        self._max = 5.12
        self._min = -self._max

    def draw_bees(self, bees, ax, iteration, best_bee, best_value):
        bee_x = [bee[0] for bee in bees]
        bee_y = [bee[1] for bee in bees]
        ax.clear()
        ax.scatter(bee_x, bee_y, s=10)
        ax.set_title(f'Лучшая точка: {np.round(best_bee, 2)},'
                     f' значение функции: {np.round(best_value, 2)}\n'
                     f'Номер итерации: {iteration}')
        ax.set_xlim([self._min, self._max])
        ax.set_ylim([self._min, self._max])

    def init_population(self):
        self.bees = (self._max - self._min) * np.random.random(size=(self.bee_count, self.n)) + self._min
        self.values = rastrigin(self.bees)

    def create_fields(self):
        self.fields = []
        visited = []
        while len(visited) < self.bee_count:
            min_index = None
            best_bee = None
            for i, bee in enumerate(self.bees):
                if i not in visited:
                    if min_index is None and best_bee is None \
                       or rastrigin(bee) < rastrigin(best_bee):
                        best_bee = bee
                        min_index = i
            current_field = []
            current_field.append(min_index)
            for i, bee in enumerate(self.bees):
                if i not in visited and i != min_index:
                    if np.linalg.norm(bee - best_bee) < self.max_distance:
                        current_field.append(i)
            self.fields.append(current_field)
            visited.extend(current_field)

    def find_field_best(self, k: int):
        cnt = 0
        new_best_bee = None
        fig, ax = plt.subplots()

        def update(frame):
            nonlocal cnt, new_best_bee
            if cnt < self.max_iter:
                field = self.fields[k]
                if new_best_bee is None:
                    current_best_bee = self.bees[self.fields[k][0]]
                else:
                    current_best_bee = new_best_bee
                min_search = np.clip(current_best_bee - self.search_size, self._min, self._max)
                max_search = np.clip(current_best_bee + self.search_size, self._min, self._max)
                new_bees = (max_search - min_search) * np.random.random(size=(self.bee_count - 1, self.n)) + min_search
                new_bees = np.vstack([new_bees, current_best_bee])
                values = rastrigin(new_bees)
                new_best_bee = new_bees[np.where(np.abs(np.min(values) - values) < 1e-10)]

                if np.linalg.norm(current_best_bee - new_best_bee) < 1e-5:
                    cnt += 1
                else:
                    cnt = 0
                self.draw_bees(new_bees, ax, cnt, new_best_bee, rastrigin(new_best_bee))
            else:
                print(new_best_bee, rastrigin(new_best_bee))
                plt.close(fig)

        ani = FuncAnimation(fig, update, frames=range(self.max_iter * self.bee_count), repeat=False)
        plt.show()

if __name__ == '__main__':
    bee_colony = BeeColony(search_size=1, max_distance=1, max_iter=30,
                           bee_count=100)
    bee_colony.init_population()
    bee_colony.create_fields()
    for i in range(len(bee_colony.fields)):
        bee_colony.find_field_best(i)