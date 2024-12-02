'''
electro.py
Реализация электромагнитного алгоритма
'''

from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray
from memory_profiler import profile as mem_profile
from line_profiler import profile as line_profile
from time import sleep


def rastrigin(x: NDArray[np.float32]) -> float:
    '''
    Вычисление функции Растригина
    '''
    return float(np.sum(x**2 - 10 * np.cos(2 * np.pi * x) + 10))
    

class EMA:
    '''
    Класс, реализующий электромагнитный алгоритм
    '''

    def __init__(self, n: int):
        self.n = n
        self.population_size = 10 * n
        self.local_iter = 10
        self.scale = 0.005
        self._min = -5.12
        self._max = -self._min
        self.x: NDArray[np.float32]
        self.values = None
        self.s = None

    @mem_profile
    def calculate_best(
            self) -> Tuple[NDArray[np.float32], float, NDArray[np.float32]]:
        '''
        Расчёт лучшего решения на итерации
        '''
        if self.s is None:
            self.s = [elem for elem in self.x for _ in range(2)]
        else:
            self.s = [elem for elem in self.s for _ in range(2)]
        for i in range(len(self.s)):
            self.s.extend([1, 1, 1])
        values = np.array([rastrigin(x) for x in self.x])
        best_value = float(np.min(values))
        best_x = self.x[np.where(abs(values - best_value) < 1e-3)].flatten()
        return values, best_value, best_x

    def create_population(self):
        '''
        Создание агентов в популяции
        '''
        self.x = np.vstack([
            self._min + np.random.uniform(0, 1, size=self.n) *
            (self._max - self._min) for _ in range(self.population_size)
        ])
        
        self.calculate_best()

    def local_search(self) -> None:
        '''
        Реализация локального поиска
        '''
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

    def calculate_force(self) -> NDArray[np.float32]:
        '''
        Расчёт электромагнитной силы
        '''
        values, best_value, _ = self.calculate_best()
        q = np.exp(-self.n * (values - best_value) /
                   (np.sum(values - best_value)))
        force = np.zeros_like(self.x)
        for i in range(self.population_size):
            for j in range(self.population_size):
                if i != j:
                    if values[j] < values[i]:
                        force[i] += (
                            ((self.x[j] - self.x[i]) /
                             np.linalg.norm(self.x[j] - self.x[i])**2) * q[i] *
                            q[j])
                    else:
                        force[i] += (
                            ((self.x[i] - self.x[j]) /
                             np.linalg.norm(self.x[j] - self.x[i])**2) * q[i] *
                            q[j])
        return force

    def move_particles(self, force) -> None:
        '''
        Передвижение частиц
        '''
        values, best_value, _ = self.calculate_best()
        for i in range(self.population_size):
            if abs(values[i] - best_value) > 1e-3:
                alpha = np.random.uniform()
                velocity = np.ones_like(self.x[i])
                normalized_force = force[i] / np.linalg.norm(force[i])
                for j in range(self.n):
                    if force[i][j] > 0:
                        velocity[j] = self._max - self.x[i][j]
                    else:
                        velocity[j] = self.x[i][j] - self._min
                self.x[i] += alpha * np.multiply(normalized_force, velocity)

    @line_profile
    def solve(self) -> None:
        '''
        Запуск алгоритма
        '''
        self.create_population()
        history = []
        max_iter = 100
        for i in range(max_iter):
            _, best_value, best_x = self.calculate_best()
            history.append(best_value)
            print(
                f'Текущее лучшее значение: {round(best_value, 4)}'
                f' в точке {list(map(lambda x: round(x, 4), best_x))}'
            )
            print(f'Итерация: {i + 1}')
            self.local_search()
            force = self.calculate_force()
            self.move_particles(force)


def main() -> None:
    '''
    Главная функция
    '''
    ema = EMA(2)
    ema.solve()


if __name__ == '__main__':
    main()
