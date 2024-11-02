import numpy as np
import matplotlib.pyplot as plt


class Solution:

    def __init__(self):
        self.current_solution: np.ndarray
        self.best_solution: np.ndarray | None = None
        self._max = 5.12
        self._min = -self._max
        self.n = 2

    @staticmethod
    def rastrigin(x: np.ndarray):
        return 10 * len(x) + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

    def init_solution(self):
        self.best_solution = self.current_solution = np.random.random(size=self.n) * (self._max - self._min) + self._min

    @staticmethod
    def cauchy_distribution(x, main_x, temperature):
        return ((1 / np.pi) * temperature / ((x - main_x) ** 2 + temperature ** 2))

    def generate_solution(self, temperature: float):
        while True:
            new_x = np.random.random(size=self.n) * (self._max - self._min) + self._min
            p_distribute = Solution.cauchy_distribution(self.best_solution, new_x, temperature)
            p = np.random.random(size=p_distribute.shape)
            if np.all(p <= p_distribute):
                return new_x

    def solve(self):
        temperature = 100
        t0 = temperature
        history = []
        history.append(self.rastrigin(self.best_solution))
        print(
            f'Исходное решение: ({", ".join(map(lambda x: str(round(x, 2)), self.current_solution))})'
        )
        print(
            f'Исходное значение функции: {self.rastrigin(self.current_solution)}')
        print('============\n')
        k = 2
        while t0 > 10:
            print(f'Температура: {t0}')
            print('=============')
            self.current_solution = self.generate_solution(temperature)
            current_rastrigin, best_rastrigin = self.rastrigin(
                self.current_solution), self.rastrigin(self.best_solution)
            print(
                f'Лучшее решение: ({", ".join(map(lambda x: str(round(x, 2)), self.best_solution))})')
            print(f'Лучшее значение функции: {best_rastrigin}')
            print(
                f'Текущее решение: ({", ".join(map(lambda x: str(round(x, 2)), self.current_solution))})'
            )
            print(f'Текущее значение функции: {current_rastrigin}')
            if current_rastrigin < best_rastrigin:
                self.best_solution = self.current_solution
            else:
                prob_lim = np.exp(-(current_rastrigin - best_rastrigin) / t0)
                probability = np.random.random()
                print(f'H = {prob_lim}; p = {probability}')
                if probability < prob_lim:
                    self.best_solution = self.current_solution
            t0 = temperature / (k ** (1 / self.n))
            k += 1
            print('===============\n')
            history.append(self.rastrigin(self.best_solution))

        best_rastrigin = self.rastrigin(self.best_solution)
        print(f'Лучшее решение: ({", ".join(map(lambda x: str(round(x, 2)), self.best_solution))})')
        print(f'Лучшее значение функции: {best_rastrigin}')
        plt.plot(history)
        plt.show()


def main():
    solution = Solution()
    solution.init_solution()
    solution.solve()


if __name__ == '__main__':
    main()
