import numpy as np
import matplotlib.pyplot as plt


def rastrigin(x: np.ndarray):
    return np.sum(x**2 - 10 * np.cos(2 * np.pi * x) + 10)


class EMA:
    def __init__(self, n: int):
        self.n = n
        self.population_size = 4
        self.max_iter = 50 * n
        self.local_iter = 10
        self.scale = 0.005
        self._min = -5.12
        self._max = -self._min

    def calculate_best(self):
        self.values = np.array([rastrigin(x) for x in self.x])
        self.best_value = np.min(self.values)
        self.best_index = np.where(abs(self.values - self.best_value) < 1e-3)[0][0]
        self.best_x = self.x[np.where(abs(self.values - self.best_value) < 1e-3)].flatten()

    def create_population(self):
        self.x = np.vstack([self._min + np.random.uniform(0, 1, size=self.n) * (self._max - self._min)
                           for _ in range(self.population_size)])
        self.calculate_best()
        for i in range(len(self.x)):
            print(f"X_{i + 1} = ({self.x[i][0]:.3f}, {self.x[i][1]:.3f}); f(X_{i}) = {self.values[i]:.3f}")
        print()

    def local_search(self):
        search_field = self.scale * (self._max - self._min)
        for k, particle in enumerate(self.x):
            cnt = 0
            while cnt < self.local_iter:
                for i in range(self.n):
                    sign = np.random.randint(0, 2) * 2 - 1
                    y = particle.copy()
                    velocity = np.random.uniform()
                    y[i] += sign * velocity * search_field
                    if rastrigin(y) < rastrigin(particle):
                        self.x[k] = y.copy()
                        cnt = self.local_iter
                        break
                    cnt += 1
        self.calculate_best()
        print('После выполнения локального поиска точки имеют следующие координаты:\n')
        for i in range(len(self.x)):
            print(f"X_{i + 1} = ({self.x[i][0]:.3f}, {self.x[i][1]:.3f}); f(X_{i}) = {self.values[i]:.3f}")
        print()
        print(f'При этом, значение \\varphi_best равно {self.best_value:.3f} в точке ({self.best_x[0]:.3f}, {self.best_x[1]:.3f}).')

    def calculate_force(self):
        q_sum = np.sum(self.values - self.best_value)
        self.q = np.exp(-self.n * (self.values - self.best_value) / (np.sum(self.values - self.best_value)))
        print('Далее приведены расчёты значения заряда для каждой из частиц по Формуле 1.1.3:\n')
        for i in range(len(self.x)):
            if i != self.best_index:
                print(f"q_{i + 1} = exp(-2 * ({self.values[i]:.3f} - {self.best_value:.3f})/{q_sum:.3f}) = {self.q[i]:.3f}")
        print()
        print('При этом, заряд у лучшей частицы будет равен единице, поскольку аргумент в экспоненте будет равен нулю.')
        print('Затем вычисляются значение силы для каждой частицы по Формуле 1.1.4:\n')
        result_str = [f"F_{i + 1} = " for i in range(self.population_size)]
        self.force = np.zeros_like(self.x)
        for i in range(self.population_size):
            for j in range(self.population_size):
                if i != j:
                    if self.values[j] < self.values[i]:
                        value = ((self.x[j] - self.x[i]) / np.linalg.norm(self.x[j] - self.x[i]) ** 2) \
                                * self.q[i] * self.q[j]
                        result_str[i] += f"{self.q[i]:.3f} * {self.q[j]:.3f} * " \
                                         f"(({', '.join(map(lambda x: str(round(x, 3)), self.x[j]))})" \
                                         f" - ({', '.join(map(lambda x: str(round(x, 3)), self.x[i]))}))" \
                                         f"/{np.linalg.norm(self.x[j] - self.x[i]) ** 2:.3f}"
                        self.force[i] += value
                    else:
                        value = ((self.x[i] - self.x[j]) / np.linalg.norm(self.x[j] - self.x[i]) ** 2) \
                                * self.q[i] * self.q[j]
                        result_str[i] += f"{self.q[i]:.3f} * {self.q[j]:.3f} * " \
                                         f"(({', '.join(map(lambda x: str(round(x, 3)), self.x[i]))})" \
                                         f" - ({', '.join(map(lambda x: str(round(x, 3)), self.x[j]))}))" \
                                         f"/{np.linalg.norm(self.x[j] - self.x[i]) ** 2:.3f}"
                        self.force[i] += value
                    if j != self.population_size - 1:
                        result_str[i] += ' + '
        for i in range(len(result_str)):
            result_str[i] += f' = ({", ".join(map(lambda x: str(round(x, 3)), self.force[i]))})'
        print('\n'.join(result_str))

    def move_particles(self):
        print(f'\nИ наконец, позиции частиц изменяются по Формулам 1.1.5-1.1.6.'
              f' Частица X_{self.best_index + 1} не передвигается, т.к. она имеет лучшее значение')
        for i in range(self.population_size):
            if abs(self.values[i] - self.best_value) > 1e-3:
                alpha = np.random.uniform()
                print(f'Рассчитаем смещение для {i + 1}-й частицы. Сгенерировано случайное число U(0;1) = {alpha:.3f}')
                velocity = np.ones_like(self.x[i])
                normalized_force = self.force[i] / np.linalg.norm(self.force[i])
                print(f'Нормированный вектор силы у {i + 1}-й частицы: F_{i + 1} ='
                      f' ({", ".join(map(lambda x: str(round(x, 3)), normalized_force))})')
                print(f'Рассчитаны компоненты вектора скорости для {i + 1}-й частицы:\n')
                for j in range(self.n):
                    if self.force[i][j] > 0:
                        velocity[j] = self._max - self.x[i][j]
                        print(f'v_{i + 1}{j + 1} = {self._max} '
                              f'{"-" if self.x[i][j] > 0 else "+"} {abs(self.x[i][j]):.3f} = {velocity[j]:.3f}')
                    else:
                        velocity[j] = self.x[i][j] - self._min
                        print(f'v_{i + 1}{j + 1} = {self.x[i][j]:.3f} + {abs(self._min)} = {velocity[j]:.3f}')
                print()
                print('Тогда частица сместится на следующую позицию:\n')
                print(f'X_{i + 1} = ({", ".join(map(lambda x: str(round(x, 3)), self.x[i]))})'
                      f' + {alpha:.3f} * ({", ".join(map(lambda x: str(round(x, 3)), normalized_force))})'
                      f' * ({", ".join(map(lambda x: str(round(x, 3)), velocity))})', end='')
                self.x[i] += alpha * np.multiply(normalized_force, velocity)
                print(f' = ({", ".join(map(lambda x: str(round(x, 3)), self.x[i]))})')
                print(f'F(X_{i + 1}) = {rastrigin(self.x[i]):.3f}\n')

    def solve(self):
        self.create_population()
        history = []
        for i in range(self.max_iter):
            history.append(self.best_value)
            self.local_search()
            self.calculate_best()
            self.calculate_force()
            self.move_particles()
            exit(0)
        plt.plot(history)
        plt.show()



def main():
    ema = EMA(2)
    ema.solve()


if __name__ == '__main__':
    main()
