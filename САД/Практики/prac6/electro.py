import numpy as np
import matplotlib.pyplot as plt


def rastrigin(x: np.ndarray):
    return np.sum(x**2 - 10 * np.cos(2 * np.pi * x) + 10)


class EMA:
    def __init__(self, n: int):
        self.n = n
        self.population_size = 10 * n
        self.max_iter = 50 * n
        self.local_iter = 10
        self.scale = 0.005
        self._min = -5.12
        self._max = -self._min

    def calculate_best(self):
        self.values = np.array([rastrigin(x) for x in self.x])
        self.best_value = np.min(self.values)
        self.best_x = self.x[np.where(abs(self.values - self.best_value) < 1e-3)].flatten()

    def create_population(self):
        self.x = np.vstack([self._min + np.random.uniform(0, 1, size=self.n) * (self._max - self._min)
                           for _ in range(self.population_size)])
        self.calculate_best()

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

    def calculate_force(self):
        self.q = np.exp(-self.n * (self.values - self.best_value) / (np.sum(self.values - self.best_value)))
        self.force = np.zeros_like(self.x)
        for i in range(self.population_size):
            for j in range(self.population_size):
                if i != j:
                    if self.values[j] < self.values[i]:
                        self.force[i] += ((self.x[j] - self.x[i]) / np.linalg.norm(self.x[j] - self.x[i]) ** 2) \
                                         * self.q[i] * self.q[j]
                    else:
                        self.force[i] += ((self.x[i] - self.x[j]) / np.linalg.norm(self.x[j] - self.x[i]) ** 2) \
                                         * self.q[i] * self.q[j]

    def move_particles(self):
        for i in range(self.population_size):
            if abs(self.values[i] - self.best_value) > 1e-3:
                alpha = np.random.uniform()
                velocity = np.ones_like(self.x[i])
                normalized_force = self.force[i] / np.linalg.norm(self.force[i])
                for j in range(self.n):
                    if self.force[i][j] > 0:
                        velocity[j] = self._max - self.x[i][j]
                    else:
                        velocity[j] = self.x[i][j] - self._min
                self.x[i] += alpha * np.multiply(normalized_force, velocity)

    def solve(self):
        self.create_population()
        history = []
        for i in range(self.max_iter):
            history.append(self.best_value)
            print(f'Текущее лучшее значение: {round(self.best_value, 4)} в точке {list(map(lambda x: round(x, 4), self.best_x))}')
            print(f'Итерация: {i + 1}')
            self.local_search()
            self.calculate_force()
            self.move_particles()
        plt.plot(history)
        plt.show()



def main():
    ema = EMA(2)
    ema.solve()


if __name__ == '__main__':
    main()
