import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random


class Path:
    graph: np.ndarray | None = None
    x: np.ndarray | None = None
    y: np.ndarray | None = None

    def __init__(self,
                 path: list[int] | None = None,
                 graph: np.ndarray | None = None,
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
            raise Exception('Ошибка с данными о графе')

    def create_new_path(self):
        while not all([x in self.path for x in range(Path.graph.shape[0])]):
            possible_places = [
                i for i in range(Path.graph.shape[0])
                if i not in self.path
            ]
            next_place = random.choice(possible_places)
            self.path.append(next_place)
        self.path.append(0)

    def get_replacements(self):
        possible_replacements = [
            self.path[i] for i in range(1, len(self.path))
            if self.path[i] != 0
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
        self.path = [elem for elem in self.path]
        self.path[first_index], self.path[second_index] = self.path[second_index], self.path[first_index]
        print(f'Замены: {self.path[first_index]}, {self.path[second_index]}')

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
        for i, point in enumerate(self.path):
            result_str += str(point)

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
    
    def draw_path(self):
        for i in range(len(Path.graph)):
            plt.text(Path.x[i], Path.y[i], f'{i}')
        for v0, v1 in zip(self.path, self.path[1:]):
            x = (Path.x[v0], Path.x[v1])
            y = (Path.y[v0], Path.y[v1])
            plt.plot(x, y)
        plt.show()


class Solution:

    def __init__(self, file_path):
        self.file_path = file_path
        self.current_path: Path
        self.best_path: Path | None = None

    def create_graph(self):
        df = pd.read_csv(self.file_path)
        # df = pd.concat([pd.DataFrame([[0, 0, 0]], columns=df.columns), df],
        #                ignore_index=True)
        x = df['x'].to_numpy()
        y = df['y'].to_numpy()
        graph = np.ndarray(shape=(len(df), len(df)))
        for i in range(len(df)):
            for j in range(len(df)):
                graph[i][j] = np.sqrt((x[i] - x[j])**2 + (y[i] - y[j])**2)
                if i < j:
                    sign_1 = '-' if x[j] >= 0 else '+'
                    sign_2 = '-' if y[j] >= 0 else '+'
                    print(f'sqrt(({x[i]} {sign_1} {abs(x[j])})^2 + ({y[i]} {sign_2} {abs(y[j])})^2) = {round(graph[i][j], 2)} \\')

        for i in range(len(df)):
            for j in range(len(df)):
                if i < j:
                    print(f'[{i} #math.arrow {j}], [{graph[i][j]: .2f}],')

        self.current_path = Path(graph=graph, x=x, y=y)
        self.current_path.create_new_path()

    def solve(self):
        temperature = 1000
        history = []
        self.best_path = self.current_path
        history.append(self.best_path.length)
        print('Начальный путь: ' + self.best_path.print_verbose())
        print(f'Длина начального пути: {self.best_path.print_length()} = {self.best_path.length:.2f} (м)')
        print('============\n')
        i = 0
        while temperature > 1:
            i += 1
            print(f'Температура: {temperature}')
            print('=============')
            self.current_path = Path(self.best_path.path)
            self.current_path.recreate_path()
            print('Лучший путь: ' + self.best_path.print_verbose())
            print(f'Длина лучшего пути: {self.best_path.length:.2f} м')
            print('Текущий путь: ' + self.current_path.print_verbose())
            print(f'Длина текущего пути: {self.current_path.print_length()} = {self.current_path.length:.2f} (м)')
            if self.current_path.length < self.best_path.length:
                self.best_path = self.current_path
            else:
                prob_lim = np.exp(-(self.current_path.length -
                                    self.best_path.length) /
                                  (temperature))
                probability = np.random.random()
                print(f'H = {prob_lim}; p = {probability}')
                if probability < prob_lim:
                    self.best_path = self.current_path
            temperature *= 0.9
            print('===============\n')
            history.append(self.best_path.length)
            
        
        print('Найденное лучшее решение: ' + self.best_path.print_verbose())
        print(f'Длина найденного решения: {self.best_path.length:.2f} m')
        plt.plot(history)
        plt.show()
        self.best_path.draw_path()


def main():
    solution = Solution('backup_6.csv')
    solution.create_graph()
    solution.solve()


if __name__ == '__main__':
    main()
