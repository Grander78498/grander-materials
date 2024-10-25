import numpy as np
import matplotlib.pyplot as plt


def rastrigin(x: np.ndarray):
    # a = x[0]
    # b = x[1]
    # return (1.5 - a + a * b) ** 2 + (2.25 - a + a * b ** 2) ** 2 + (2.625 - a + a * b ** 3) ** 2
    return 10 * len(x) + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))


class BeeColony:

    def __init__(self,
                 scout_bee_count: int = 10,
                 optimal_bee_count: int = 5,
                 suboptimal_bee_count: int = 2,
                 optimal_solution_count: int = 2,
                 suboptimal_solution_count: int = 3,
                 field_size: float = 1.5):
        self.scout_bee_count = scout_bee_count
        self.optimal_bee_count = optimal_bee_count
        self.suboptimal_bee_count = suboptimal_bee_count
        self.optimal_solution_count = optimal_solution_count
        self.suboptimal_solution_count = suboptimal_solution_count
        self.field_size = field_size

        self._max = 5.12
        self._min = -self._max
        self.n = 2

    def solution_step(self, previous_result: np.ndarray | None = None):
        if previous_result is None:
            bee_area = np.random.random(size=(self.scout_bee_count, self.n)
                                        ) * (self._max - self._min) + self._min
        else:
            bee_area = previous_result
        function_values = np.array([rastrigin(x) for x in bee_area])
        bee_area = bee_area[function_values.argsort()]

        optimal_solution = bee_area[:self.optimal_solution_count]
        suboptimal_solution = bee_area[self.optimal_solution_count:self.
                                       optimal_solution_count +
                                       self.suboptimal_solution_count]

        new_bee_area = []
        for solution in optimal_solution:
            min_search_field = solution - self.field_size
            max_search_field = solution + self.field_size
            new_bee_area.append(solution)
            for _ in range(self.optimal_bee_count - 1):
                bee = np.random.random(self.n) * (
                    max_search_field - min_search_field) + min_search_field
                new_bee_area.append(bee)

        for solution in suboptimal_solution:
            min_search_field = solution - self.field_size
            max_search_field = solution + self.field_size
            new_bee_area.append(solution)
            for _ in range(self.suboptimal_bee_count - 1):
                bee = np.random.random(self.n) * (
                    max_search_field - min_search_field) + min_search_field
                new_bee_area.append(bee)
        return np.array(new_bee_area)


class Solution:

    def __init__(self):
        self.bee_colony = BeeColony(scout_bee_count=100,
                                    optimal_bee_count=30,
                                    suboptimal_bee_count=10,
                                    optimal_solution_count=10,
                                    suboptimal_solution_count=5,
                                    field_size=0.5)

    def solve(self):
        history = []
        result: np.ndarray | None = None
        best_result_value = float("inf")
        best_result_repeat = 0
        while result is None or best_result_repeat < 1000:
            result = self.bee_colony.solution_step(result)
            function_values = np.array([rastrigin(x) for x in result])
            if np.min(function_values) < best_result_value:
                best_result_value = np.min(function_values)
                best_result = result[function_values.argmin()]
                best_result_repeat = 0
                history.append(best_result_value)
            else:
                best_result_repeat += 1
            print(
                f'Лучший результат {best_result_value} в точке {best_result}.'
                f' Количество повторений: {best_result_repeat}')
        plt.plot(history)
        plt.show()


def main():
    solution = Solution()
    solution.solve()


if __name__ == '__main__':
    main()
