import numpy as np
import matplotlib.pyplot as plt


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

    def draw_bees(self, bees):
        bee_x = [bee[0] for bee in bees]
        bee_y = [bee[1] for bee in bees]
        ax = plt.gca()
        for i in range(len(self.bees)):
            ax.annotate(str(i), (bees[i][0], bees[i][1]))
        plt.scatter(bee_x, bee_y, s=10)
        plt.show()

    def init_population(self):
        self.bees = (self._max - self._min) * np.random.random(size=(self.bee_count, self.n)) + self._min
        self.values = rastrigin(self.bees)

        for i in range(len(self.bees)):
            print(f"X_{i + 1} = ({self.bees[i][0]:.3f}, {self.bees[i][1]:.3f}); f(X_{i}) = {self.values[i]:.3f}")
        print()

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
            print(f"Среди оставшихся точек лучшее значение имеется у пчелы X_{min_index + 1}: значение функции у неё равно {rastrigin(best_bee):.3f}.")
            if len(visited) + 1 == self.bee_count:
                print(f'Поскольку точек больше не осталось, то точка X_{min_index + 1} образует область сама с собой.')
            else:
                print(f"Далее рассчитывается Евклидово расстояние между точкой X_{min_index + 1} и оставшимися точками по Формуле 1.1.2.")
            print()
            current_field = []
            current_field.append(min_index)
            for i, bee in enumerate(self.bees):
                if i not in visited and i != min_index:
                    print(f"d_({min_index + 1} {i + 1}) = \\sqrt("
                          f"({best_bee[0]:.3f} {'-' if bee[0] > 0 else '+'} {abs(bee[0]):.3f})^2 +"
                          f" ({best_bee[1]:.3f} {'-' if bee[1] > 0 else '+'} {abs(bee[1]):.3f})^2) = "
                          f"{np.linalg.norm(bee - best_bee):.3f}", end='')
                    if np.linalg.norm(bee - best_bee) < self.max_distance:
                        print(" < ", end='')
                        current_field.append(i)
                    else:
                        print(" >= ", end='')
                    print(f"{self.max_distance}")
            print()
            if len(current_field) > 2:
                print(f'Следовательно, в область точки X_{min_index + 1} вошли точки'
                      f' {", ".join("X_" + str(elem + 1) for elem in current_field[1:])}')
            elif len(current_field) == 2:
                print(f'Следовательно, в область точки X_{min_index + 1} вошла точка'
                      f' {", ".join("X_" + str(elem + 1) for elem in current_field[1:])}')
            elif len(visited) + 1 != self.bee_count:
                print(f'Следовательно, точка X_{min_index + 1} образует область сама с собой.')
            self.fields.append(current_field)
            visited.extend(current_field)

    def find_field_best(self, k: int):
        print(f'Рассмотрим поиск в первой подобласти.'
              f' Лучшая точка: ({self.bees[self.fields[k][0]][0]:.3f}, {self.bees[self.fields[k][0]][1]:.3f}) '
              f'со значением функции {rastrigin(self.bees[self.fields[k][0]]):.3f}.')
        print(f'Новые сгенерированные точки имеют следующие координаты (точка X_{self.bee_count} является текущим центром области):\n')
        cnt = 0
        new_best_bee = None
        while cnt < self.max_iter:
            if new_best_bee is None:
                current_best_bee = self.bees[self.fields[k][0]]
            else:
                current_best_bee = new_best_bee
            min_search = np.clip(current_best_bee - self.search_size, self._min, self._max)
            max_search = np.clip(current_best_bee + self.search_size, self._min, self._max)
            new_bees = (max_search - min_search) * np.random.random(size=(self.bee_count - 1, self.n)) + min_search
            new_bees = np.vstack([new_bees, current_best_bee])
            values = rastrigin(new_bees)
            for i in range(len(new_bees)):
                print(f"X_{i + 1} = ({new_bees[i][0]:.3f}, {new_bees[i][1]:.3f}); f(X_{i}) = {values[i]:.3f}")
            print()
            min_index = np.where(np.abs(np.min(values) - values) < 1e-10)[0][0]
            new_best_bee = new_bees[np.where(np.abs(np.min(values) - values) < 1e-10)[0]]
            print(f'Минимальное значение среди достигнуто точкой X_{min_index + 1}'
                  f' (значение функции равно {rastrigin(new_best_bee)[0]:.3f}).'
                  f' Следовательно, эта точка становится центром области, и происходит переход к новой итерации.')

            if np.linalg.norm(current_best_bee - new_best_bee) < 1e-5:
                cnt += 1
            else:
                cnt = 0
            exit(0)
        print(new_best_bee, rastrigin(new_best_bee))



if __name__ == '__main__':
    bee_colony = BeeColony(search_size=1, max_distance=2, max_iter=100,
                           bee_count=10)
    bee_colony.init_population()
    bee_colony.create_fields()
    for i in range(len(bee_colony.fields)):
        bee_colony.find_field_best(i)