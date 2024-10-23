import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


class Path:
    weights: np.ndarray | None = None
    graph: np.ndarray | None = None
    max_weight = 6

    def __init__(self,
                 path: list[int] | None = None,
                 weights: np.ndarray | None = None,
                 graph: np.ndarray | None = None):
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

    def create_new_path(self, current_weight: int = 0):
        while not all([x in self.path for x in range(Path.graph.shape[0])]):
            possible_weights = [
                i for i in range(len(Path.weights))
                if Path.weights[i] <= (Path.max_weight - current_weight) and (
                    i not in self.path or i == 0)
            ]
            while True:
                next_place = random.choice(possible_weights)
                if next_place == 0:
                    if self.path[-1] == 0:
                        continue
                    current_weight = 0
                else:
                    next_weight = Path.weights[next_place]
                    current_weight += next_weight
                break
            self.path.append(next_place)
        self.path.append(0)

    def get_replacements(self):
        possible_replacements = [
            self.path[i] for i in range(1, len(self.path))
            if self.path[i - 1] == 0
        ]
        while True:
            first, second = random.choices(possible_replacements, k=2)
            if first != second:
                break
        first_index, second_index = self.path.index(first), self.path.index(
            second)
        if first_index > second_index:
            first_index, second_index = second_index, first_index
            first, second = second, first
        return first_index, second_index

    def recreate_path(self):
        first_index, second_index = self.get_replacements()
        first, second = self.path[first_index], self.path[second_index]
        print(f'Replaces: {first}, {second}')

        self.path = self.path[:first_index + 1]
        self.path[-1] = second
        current_weight = Path.weights[second]
        self.create_new_path(current_weight=current_weight)

    @property
    def length(self) -> float:
        length = 0
        for i in range(1, len(self.path)):
            length += Path.graph[self.path[i]][self.path[i - 1]]
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
            edge_len = Path.graph[self.path[i]][self.path[i - 1]]
            if not cum_length:
                cum_length.append(edge_len)
            else:
                cum_length.append(edge_len)
        return " + ".join(map(lambda x: str(round(x, 2)), cum_length))


class Solution:

    def __init__(self, file_path):
        self.file_path = file_path
        self.current_path: Path
        self.best_path: Path | None = None

    def create_graph(self):
        df = pd.read_csv('data.csv')
        df = pd.concat([pd.DataFrame([[0, 0, 0]], columns=df.columns), df],
                       ignore_index=True)
        weights = df['weight'].to_numpy()
        x = df['x'].to_numpy()
        y = df['y'].to_numpy()
        graph = np.ndarray(shape=(len(df), len(df)))
        for i in range(len(df)):
            for j in range(len(df)):
                graph[i][j] = np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
                if i < j:
                    print(round(graph[i][j], 2))

        self.current_path = Path(weights=weights, graph=graph)
        self.current_path.create_new_path()

    def solve(self):
        temperature = 100
        history = []
        self.best_path = self.current_path
        history.append(self.best_path.length)
        print('Initial path: ' + self.best_path.print_verbose())
        print(f'Initial length: {self.best_path.print_length()} = {self.best_path.length:.2f} m')
        print('============\n')
        while temperature > 0.0000001:
            print(f'Temperature: {temperature}')
            print('=============')
            self.current_path = Path(self.best_path.path)
            self.current_path.recreate_path()
            print('Best path: ' + self.best_path.print_verbose())
            print(f'Best length: {self.best_path.length:.2f} m')
            print('Current path: ' + self.current_path.print_verbose())
            print(f'Current length: {self.current_path.print_length()} = {self.current_path.length:.2f} м')
            if self.current_path.length < self.best_path.length:
                self.best_path = self.current_path
            else:
                prob_lim = np.exp(-(self.current_path.length -
                                    self.best_path.length) /
                                  (1000 * temperature))
                probability = np.random.random()
                print(f'H = {prob_lim}; p = {probability}')
                if probability < prob_lim:
                    self.best_path = self.current_path
            temperature /= 2
            print('===============\n')
            history.append(self.best_path.length)
        
        print('Best path: ' + self.best_path.print_verbose())
        print(f'Best length: {self.best_path.length:.2f} m')
        plt.plot(history)
        plt.show()


def main():
    solution = Solution('data.csv')
    solution.create_graph()
    solution.solve()


if __name__ == '__main__':
    main()
