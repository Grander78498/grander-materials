import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import time
from math import sqrt


max_weight = 6


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
            raise Exception('Stupid motherfucker')

    def create_new_path(self, alpha: float, beta: float):
        self.path = [0]
        # self.path = [random.randint(0, len(Path.graph) - 1)]
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
            next_place = np.random.choice(possible_places, p=pheromones)
            self.path.append(next_place)
            continue

            total_probability = 0
            for next_place, pher in zip(possible_places, pheromones):
                total_probability += pher / total_pheromone
                probability = random.random()
                if probability < total_probability:
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

    def print_verbose(self):
        result_str = ''
        for i, point in enumerate(self.path):
            result_str += str(point)

            if i != len(self.path) - 1:
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
        self.beta = 5

    def solution_step(self):
        for ant in self.ants:
            ant.create_new_path(self.alpha, self.beta)
            print(ant.print_verbose())

        for i in range(len(Path.graph)):
            for j in range(len(Path.graph)):
                Path.graph[i][j].pheromone *= (1 - self.vapor_rate)
        
        for ant in self.ants:
            delta_pheromone = np.exp(1 / ant.length)
            for i, j in zip(ant.path, ant.path[1:]):
                Path.graph[i][j].pheromone = Path.graph[i][j].pheromone + delta_pheromone
                Path.graph[j][i].pheromone = Path.graph[j][i].pheromone + delta_pheromone

        for i in range(len(Path.graph)):
            for j in range(len(Path.graph)):
                Path.graph[i][j].pheromone *= self.vapor_rate


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
        df = pd.read_csv('../prac2/data.csv')
        # df = pd.concat([pd.DataFrame([[0, 0, 0]], columns=df.columns), df],
        #                ignore_index=True)
        x = df['x'].to_numpy()
        y = df['y'].to_numpy()
        self.graph = graph = [[GraphElement() for _ in range(len(df))] for _ in range(len(df))]
        pheromone = random.random()
        for i in range(len(df)):
            for j in range(i, len(df)):
                graph[i][j].distance = graph[j][i].distance = sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
                if i != j:
                    graph[i][j].pheromone = graph[j][i].pheromone = pheromone

        Path(graph=graph, x=x, y=y)

    def solve(self):
        ant_colony = AntColony(ant_count=len(self.graph))
        steps = 100
        history = []
        for step in range(steps):
            print(f'Итерация {step + 1} / {steps}')
            current_path = ant_colony.solution_step()
            if self.best_path is None or current_path.length < self.best_path.length:
                self.best_path = current_path
            history.append(self.best_path.length)
            print(f'Лучший путь: {self.best_path.print_verbose()}')
            print(f'Длина лучшего пути: {self.best_path.length}')
            print('\n\n\n')
        plt.plot(history)
        plt.show()
        self.best_path.draw_path()
        


def main():
    solution = Solution('data.csv')
    solution.create_graph()
    solution.solve()


if __name__ == '__main__':
    main()
