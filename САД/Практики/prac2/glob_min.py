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
        temperature = 2
        t0 = temperature
        history = []
        history.append(self.rastrigin(self.best_solution))
        print(
            f'Initial solution: ({", ".join(map(str, self.current_solution))})'
        )
        print(
            f'Initial function value: {self.rastrigin(self.current_solution)}')
        print('============\n')
        for k in range(2, 301):
            print(f'Temperature: {t0}')
            print('=============')
            self.current_solution = self.generate_solution(temperature)
            current_rastrigin, best_rastrigin = self.rastrigin(
                self.current_solution), self.rastrigin(self.best_solution)
            print(
                f'Best solution: ({", ".join(map(str, self.best_solution))})')
            print(f'Best function value: {best_rastrigin}')
            print(
                f'Current solution: ({", ".join(map(str, self.current_solution))})'
            )
            print(f'Current function value: {current_rastrigin}')
            if current_rastrigin < best_rastrigin:
                self.best_solution = self.current_solution
            else:
                prob_lim = np.exp(-(current_rastrigin - best_rastrigin) / t0)
                probability = np.random.random()
                print(f'H = {prob_lim}; p = {probability}')
                if probability < prob_lim:
                    self.best_solution = self.current_solution
            t0 = temperature / (k ** (1 / self.n))
            print('===============\n')
            history.append(self.rastrigin(self.best_solution))

        best_rastrigin = self.rastrigin(self.best_solution)
        print(f'Best solution: ({", ".join(map(str, self.best_solution))})')
        print(f'Best function value: {best_rastrigin}')
        plt.plot(history)
        plt.show()


def main():
    solution = Solution()
    solution.init_solution()
    solution.solve()


if __name__ == '__main__':
    main()
