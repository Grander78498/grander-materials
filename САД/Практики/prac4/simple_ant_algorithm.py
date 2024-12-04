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
        self.path = [start_position]
        while not all([x in self.path for x in range(len(Path.graph))]):
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

            probability = np.random.random()
            total = 0
            for next_place, ph in zip(possible_places, pheromones):
                total += ph
                if probability <= total:
                    self.path.append(next_place)
                    break
        
        self.path.append(self.path[0])

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
        self.vapor_rate = 0.95
        self.alpha = 6
        self.beta = 7

    def solution_step(self):
        for i, ant in enumerate(self.ants):
            ant.create_new_path(self.alpha, self.beta, i)
            # print(ant.print_verbose())
        
        for i in range(len(Path.graph)):
            for j in range(len(Path.graph)):
                if i != j:
                    Path.graph[i][j].pheromone *= (1 - self.vapor_rate)

        delta_pheromones = [[0 for _ in range(len(Path.graph))] for _ in range(len(Path.graph))]
        for ant in self.ants:
            delta_pheromone = 100 / ant.length
            for i, j in zip(ant.path, ant.path[1:]):
                delta_pheromones[i][j] += delta_pheromone

        for i in range(len(Path.graph)):
            for j in range(len(Path.graph)):
                Path.graph[i][j].pheromone += delta_pheromones[i][j]


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
        df = pd.read_csv(self.file_path)
        x = df['x'].to_numpy()
        y = df['y'].to_numpy()
        self.graph = graph = [[GraphElement() for _ in range(len(df))] for _ in range(len(df))]
        pheromone = 0.78498
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
        ant_colony = AntColony(ant_count=len(Path.graph))
        steps = 40
        history = []
        mean_history = []
        for step in range(steps):
            print(f'Итерация {step + 1} / {steps}')
            if (step + 1) % (steps // 5) == 0 or step == 0:
                for ant in ant_colony.ants:
                    print(ant.print_verbose(start_at_zero=True))
                    print(ant.length)
            current_path = ant_colony.solution_step()
            mean = 0
            for ant in ant_colony.ants:
                mean += ant.length
            mean /= len(ant_colony.ants)
            mean_history.append(mean)
            if self.best_path is None or current_path.length < self.best_path.length:
                self.best_path = current_path
            history.append(self.best_path.length)
            print(f'Лучший путь: {self.best_path.print_verbose(start_at_zero=True)}')
            print(f'Длина лучшего пути: {self.best_path.length}')
            print('\n\n\n')
        fig, ax = plt.subplots()
        ax.set_title(f'Длина лучшего пути: {self.best_path.length:.2f}')
        plt.plot(history, label='Длина лучшего пути')
        plt.plot(mean_history, label='Средняя длина пути среди муравьёв')
        plt.legend(loc='upper right')
        plt.show()
        self.best_path.draw_path()
        


def main():
    solution = Solution('../prac2/backup_10.csv')
    solution.create_graph()
    solution.solve()


if __name__ == '__main__':
    main()
