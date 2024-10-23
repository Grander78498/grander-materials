import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
from math import sqrt
from tqdm import tqdm


max_weight = 6


class GraphElement:
    def __init__(self, distance: float | None = None, pheromone: float = 0):
        self.distance = distance
        self.pheromone = pheromone


class Path:
    weights: np.ndarray | None = None
    graph: list[list[GraphElement]] | None = None

    def __init__(self,
                 path: list[int] | None = None,
                 weights: np.ndarray | None = None,
                 graph: list[list[GraphElement]] | None = None):
        if path is None:
            self.path = [0]
        else:
            self.path = path

        if Path.weights is None:
            Path.weights = weights
        if Path.graph is None:
            Path.graph = graph

        if Path.weights is None or Path.graph is None:
            raise Exception('Stupid motherfucker')

    def create_new_path(self, alpha: float):
        current_weight = 0
        self.path = [0]
        while not all([x in self.path for x in range(len(Path.graph))]):
            current_place = self.path[-1]
            possible_places = [
                i for i in range(len(Path.weights))
                if Path.weights[i] <= (max_weight - current_weight) and (
                    i not in self.path or i == 0)
            ]
            total_pheromone = 0
            for next_place in possible_places:
                total_pheromone += Path.graph[current_place][next_place].pheromone ** alpha

            total_probability = 0
            probability = random.random()
            for next_place in possible_places:
                total_probability += Path.graph[current_place][next_place].pheromone ** alpha / total_pheromone
                if probability < total_probability:
                    if next_place != current_place:
                        self.path.append(next_place)
                        if next_place == 0:
                            current_weight = 0
                        else:
                            next_weight = Path.weights[next_place]
                            current_weight += next_weight
                    break
            
        self.path.append(0)

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
        cum_weight = 0
        for i, point in enumerate(self.path):
            result_str += str(point)
            if point == 0:
                cum_weight = 0
                result_str += " (0)"
            else:
                cum_weight += Path.weights[point]
                result_str += f" ({cum_weight:.2f})"

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


class Ant:
    def __init__(self):
        self.path = Path()


class AntColony:
    def __init__(self, ant_count: int = 10):
        self.ants = [Path() for _ in range(ant_count)]
        self.vapor_rate = 0.05
        self.alpha = 2

    def solution_step(self):
        for ant in tqdm(self.ants):
            ant.create_new_path(self.alpha)
        
        for ant in self.ants:
            delta_pheromone = 1 / ant.length
            for i, j in zip(ant.path, ant.path[1:]):
                Path.graph[i][j].pheromone = Path.graph[i][j].pheromone * self.vapor_rate + delta_pheromone
                Path.graph[j][i].pheromone = Path.graph[j][i].pheromone * self.vapor_rate + delta_pheromone

        for i in range(len(Path.graph)):
            for j in range(len(Path.graph)):
                Path.graph[i][j].pheromone *= (1 - self.vapor_rate)

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
        df = pd.concat([pd.DataFrame([[0, 0, 0]], columns=df.columns), df],
                       ignore_index=True)
        weights = df['weight'].to_numpy()
        x = df['x'].to_numpy()
        y = df['y'].to_numpy()
        graph = [[GraphElement() for _ in range(len(df))] for _ in range(len(df))]
        for i in range(len(df)):
            for j in range(i, len(df)):
                graph[i][j].distance = graph[j][i].distance = sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
                if i != j:
                    graph[i][j].pheromone = graph[j][i].pheromone = random.random()

        Path(weights=weights, graph=graph)

    def solve(self):
        ant_colony = AntColony(ant_count=100)
        steps = 200
        history = []
        for step in range(steps):
            print(f'Итерация {step + 1} / {steps}')
            current_path = ant_colony.solution_step()
            if self.best_path is None or current_path.length < self.best_path.length:
                self.best_path = current_path
            history.append(self.best_path.length)
            print(f'Лучший путь: {self.best_path.print_verbose()}')
            print(f'Длина лучшего пути: {self.best_path.length}')
        plt.plot(history)
        plt.show()
        


def main():
    solution = Solution('data.csv')
    solution.create_graph()
    solution.solve()


if __name__ == '__main__':
    main()
