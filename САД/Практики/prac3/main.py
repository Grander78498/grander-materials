import numpy as np
import matplotlib.pyplot as plt


def rastrigin(x: np.ndarray):
    return 10 * len(x) + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))


class Particle:
    def __init__(self):
        self._max = 5.12
        self._min = -self._max
        self.n = 2
        self.x = np.random.random(size=self.n) * (self._max - self._min) + self._min
        self.best_x = self.x.copy()
        self.speed = np.zeros(shape=(self.n,))

    def correct_speed(self, global_best: np.ndarray):
        c1 = 2
        c2 = 2
        alpha = np.random.random()
        self.speed += c1 * alpha * (self.best_x - self.x) + c2 * (1 - alpha) * (global_best - self.x)

    def correct_position(self):
        self.x += self.speed

    def __str__(self):
        return f"Current position: {self.x} -- best position: {self.best_x}"


class Swarm:
    def __init__(self, particle_count: int = 10):
        self.particles = [Particle() for _ in range(particle_count)]
        self.best_solution: np.ndarray | None = None

    def solution_step(self):
        if self.best_solution is None:
            self.best_solution = self.particles[0].best_x.copy()

        for particle in self.particles:
            if rastrigin(particle.x) < rastrigin(particle.best_x):
                particle.best_x = particle.x.copy()
            if rastrigin(particle.best_x) < rastrigin(self.best_solution):
                self.best_solution = particle.best_x.copy()

        for particle in self.particles:
            particle.correct_speed(self.best_solution)
            particle.correct_position()

        return rastrigin(self.best_solution), self.best_solution
    
    def draw_swarm(self):
        particle_x = [particle.x[0] for particle in self.particles]
        particle_y = [particle.x[1] for particle in self.particles]
        ax = plt.gca()
        ax.set_xlim(-5.12, 5.12)
        ax.set_ylim(-5.12, 5.12)
        plt.scatter(particle_x, particle_y)
        plt.show()


class Solution:

    def __init__(self):
        self.swarm = Swarm(particle_count=100)

    def solve(self):
        steps = 200
        history = []
        for step in range(steps):
            value, x = self.swarm.solution_step()
            print(f'Итерация: {step + 1}. Значение: {value} в точке {x}')
            history.append(value)
            # if step % 20 == 0:
            #     self.swarm.draw_swarm()
        plt.plot(history)
        plt.show()


def main():
    solution = Solution()
    solution.solve()


if __name__ == '__main__':
    main()