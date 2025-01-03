import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from math import sqrt


class GraphElement:
    def __init__(self, distance: float | None = None, pheromone: float = 0):
        self.distance = distance
        self.pheromone = pheromone


class Path:
    graph: list[list[GraphElement]] | None = None
    x: np.ndarray | None = None
    y: np.ndarray | None = None

    def __init__(self,
                 path: list[int] | None = None,
                 graph: list[list[GraphElement]] | None = None,
                 x: np.ndarray | None = None,
                 y: np.ndarray | None = None):
        if path is None:
            self.path = [0]
        else:
            self.path = path

        if Path.graph is None:
            Path.graph = graph
        if Path.x is None:
            Path.x = x
        if Path.y is None:
            Path.y = y

        if Path.graph is None:
            raise Exception('Граф не построен')

    def create_new_path(self, alpha: float, beta: float, start_position: int = 0):
        self.path = [0]
        order = {0: 'первого', 1: 'второго'}
        while not all([x in self.path for x in range(len(Path.graph))]):
            print(f"Далее приведены расчёты вероятностей перехода {order[start_position]} муравья c {self.path[-1] + 1}-й вершины:\n")
            current_place = self.path[-1]
            possible_places = [
                i for i in range(len(Path.graph))
                if i not in self.path
            ]
            pheromones = []
            for next_place in possible_places:
                pheromones.append((Path.graph[current_place][next_place].pheromone ** alpha 
                                    * (1 / Path.graph[current_place][next_place].distance) ** beta))
            total_pheromone = sum(pheromones)
            pheromones = [elem / total_pheromone for elem in pheromones]
            for next_place, ph in zip(possible_places, pheromones):
                print(f"p^{start_position + 1}_{current_place + 1}{next_place + 1} = "
                    f"({Path.graph[current_place][next_place].pheromone:.3f}^{alpha}"
                    f" * {100 / Path.graph[current_place][next_place].distance:.3f}^{beta})"
                    f"/({total_pheromone:.5f}) = "
                    f"{ph:.3f}")
            print()

            probability = np.random.random()
            total = 0
            print(f'Сгенерировано случайное число r = {probability:.3f}, которое определяет,'
                  f' на какую из вершин будет совершён переход. Для этого рассчитанные вероятности'
                  f' складываются в накопительную сумму.\n')
            for next_place, ph in zip(possible_places, pheromones):
                total += ph
                print(f'P_{next_place + 1} = {total:.3f}', end='')
                if probability <= total:
                    print(f' >= r = {probability:.3f}')
                    print(f'\nПроисходит переход на вершину {next_place + 1}.', end=' ')
                    self.path.append(next_place)
                    break
                else:
                    print(f' < r = {probability:.3f}')
        
        self.path.append(self.path[0])
        print(f'Затем муравей возвращается на начальную вершину, и его путь завершается. '
              f'Таким образом, путь {order[start_position]} муравья выглядит следующим образом: {self.print_verbose()}. '
              f'Длина пути равна: {self.print_length()}.')

    @property
    def length(self) -> float:
        length = 0
        for i in range(1, len(self.path)):
            length += Path.graph[self.path[i]][self.path[i - 1]].distance
        return length

    def __str__(self) -> str:
        return ', '.join(map(str, self.path))

    def print_verbose(self, start_at_zero: bool = False):
        result_str = ''
        if start_at_zero:
            if self.path.index(0) != 0:
                index = self.path.index(0)
                first_part = self.path[index:]
                second_part = self.path[1:index]
                path = first_part + second_part + [0]
            else:
                path = self.path
        else:
            path = self.path
        for i, point in enumerate(path):
            result_str += str(point)

            if i != len(path) - 1:
                result_str += ' -> '
        return result_str

    def print_length(self):
        cum_length = []
        for i in range(1, len(self.path)):
            edge_len = Path.graph[self.path[i]][self.path[i - 1]].distance
            if not cum_length:
                cum_length.append(edge_len)
            else:
                cum_length.append(edge_len)
        return " + ".join(map(lambda x: str(round(x, 2)), cum_length))
    
    def draw_path(self):
        for i in range(len(Path.graph)):
            plt.text(Path.x[i], Path.y[i], f'{i}')
        for v0, v1 in zip(self.path, self.path[1:]):
            x = (Path.x[v0], Path.x[v1])
            y = (Path.y[v0], Path.y[v1])
            plt.plot(x, y)
        plt.show()


class Ant:
    def __init__(self):
        self.path = Path()


class AntColony:
    def __init__(self, ant_count: int = 10):
        self.ants = [Path() for _ in range(ant_count)]
        self.vapor_rate = 0.5
        self.alpha = 1
        self.beta = 2

    def solution_step(self, num_iter: int = 0):
        for i, ant in enumerate(self.ants):
            ant.create_new_path(self.alpha, self.beta, i)
            # print(ant.print_verbose())
        
        if num_iter == 0:
            print('Затем выполняется испарение феромона по Формуле 1.1.2:\n')
        else:
            print('Затем выполняется испарение феромона по Формуле 1.1.2 аналогично предыдущей итерации.')
        for i in range(len(Path.graph)):
            for j in range(len(Path.graph)):
                if i != j:
                    if num_iter == 0:
                        print(f'\\tau_{i + 1}{j + 1} = (1 - {self.vapor_rate}) * {Path.graph[i][j].pheromone:.3f} = ', end='')
                        Path.graph[i][j].pheromone *= (1 - self.vapor_rate)
                        print(f'{Path.graph[i][j].pheromone:.3f}')
                    else:
                        Path.graph[i][j].pheromone *= (1 - self.vapor_rate)
        print()
        
        print('Изменение концентрации феромона происходит по Формуле 1.1.3, где значение Q принято за 100.'
              ' Далее отображены только значения феромонов, которые после данной итерации изменились на ненулевую величину.\n')
        delta_pheromones = [[0 for _ in range(len(Path.graph))] for _ in range(len(Path.graph))]
        for ant in self.ants:
            delta_pheromone = 100 / ant.length
            for i, j in zip(ant.path, ant.path[1:]):
                delta_pheromones[i][j] += delta_pheromone

        for i in range(len(Path.graph)):
            for j in range(len(Path.graph)):
                if delta_pheromones[i][j] != 0:
                    print(f'\\tau_{i + 1}{j + 1} = {Path.graph[i][j].pheromone:.3f} + {delta_pheromones[i][j]:.3f} = ', end='')
                    Path.graph[i][j].pheromone += delta_pheromones[i][j]
                    print(f'{Path.graph[i][j].pheromone:.3f}')
        print()


        best_path = self.ants[0]
        best_length = best_path.length
        for ant in self.ants[1:]:
            if ant.length < best_length:
                best_path = ant
                best_length = best_path.length
        
        return Path(best_path.path)


class Solution:

    def __init__(self, file_path):
        self.file_path = file_path
        self.best_path: Path | None = None

    def create_graph(self):
        df = pd.read_csv('../prac2/backup_6.csv')
        x = df['x'].to_numpy()
        y = df['y'].to_numpy()
        self.graph = graph = [[GraphElement() for _ in range(len(df))] for _ in range(len(df))]
        pheromone = 0.876
        d = []
        for i in range(len(df)):
            for j in range(i, len(df)):
                graph[i][j].distance = graph[j][i].distance = sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
                if i < j:
                    sign_1 = '-' if x[j] >= 0 else '+'
                    sign_2 = '-' if y[j] >= 0 else '+'
                    print(f'\sqrt (({x[i]} {sign_1} {abs(x[j])})^2 + ({y[i]} {sign_2} {abs(y[j])})^2) = {round(graph[i][j].distance, 2)}')
                    d.append(round(graph[i][j].distance, 2))
                if i != j:
                    graph[i][j].pheromone = graph[j][i].pheromone = pheromone
        print('\n'.join(map(str, d)))
        Path(graph=graph, x=x, y=y)

    def solve(self):
        ant_colony = AntColony(ant_count=2)
        steps = 2
        history = []
        for step in range(steps):
            print(f'Итерация {step + 1} / {steps}')
            if (step + 1) % 1 == 0 or step == 0:
                for ant in ant_colony.ants:
                    print(ant.print_verbose(start_at_zero=True))
                    print(ant.length)
            current_path = ant_colony.solution_step(step)
            if self.best_path is None or current_path.length < self.best_path.length:
                self.best_path = current_path
            history.append(self.best_path.length)
            print(f'Лучший путь: {self.best_path.print_verbose(start_at_zero=True)}')
            print(f'Длина лучшего пути: {self.best_path.length}')
            print('\n\n\n')
        fig, ax = plt.subplots()
        ax.set_title(f'Длина лучшего пути: {self.best_path.length}')
        plt.plot(history)
        plt.show()
        self.best_path.draw_path()

        # for i in range(len(Path.graph)):
        #     print(" || ".join(f"{Path.graph[i][j].pheromone}" for j in range(len(Path.graph))))
        


def main():
    solution = Solution('data.csv')
    solution.create_graph()
    solution.solve()


if __name__ == '__main__':
    main()
