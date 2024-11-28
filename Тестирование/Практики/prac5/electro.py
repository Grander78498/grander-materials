import numpy as np

MAX = 5.12
MIN = -5.12
N = 9
POPULATION_SIZE = 10 * N
MAX_ITER = 50 * N
LOCAL_ITER = 10
SCALE = 0.005
X = np.zeros((N, POPULATION_SIZE))
VALUES = np.zeros(POPULATION_SIZE)
BEST_VALUE = 0
BEST_X = np.zeros(N)
FORCE = np.zeros((N, POPULATION_SIZE))




def rastrigin(x: np.ndarray):
    return np.sum(x**2 - 10 * np.cos(2 * np.pi * x) + 10)




def calculate_best():
    global VALUES, BEST_VALUE, BEST_X
    VALUES = np.array([rastrigin(x) for x in X])
    BEST_VALUE = np.min(VALUES)
    BEST_X = X[np.where(abs(VALUES - BEST_VALUE) < 1e-3)].flatten()




def create_population():
    global X
    X = np.vstack([
        MIN + np.random.uniform(0, 1, size=N) * (MAX - MIN)
        for _ in range(POPULATION_SIZE)
    ])
    calculate_best()




def local_search():
    search_field = SCALE * (MAX - MIN)
    unused = 0
    for k, particle in enumerate(X):
        cnt = 0
        while True:
            for i in range(N):
                sign = np.random.randint(0, 2) * 2 - 1
                y = particle.copy()
                velocity = np.random.uniform()
                y[i] += sign * velocity * search_field
                if rastrigin(y) < rastrigin(particle):
                    X[k] = y.copy()
                    cnt = LOCAL_ITER
                    break
                cnt += 1
    calculate_best()




def calculate_force():
    global FORCE
    q = np.exp(-N * (VALUES - BEST_VALUE) / (np.sum(VALUES - BEST_VALUE)))
    FORCE = np.zeros_like(X)
    for i in range(POPULATION_SIZE):
        for j in range(POPULATION_SIZE):
            if i != j:
                if VALUES[j] < VALUES[i]:
                    FORCE[i] += ((
                        (X[j] - X[i]) / np.linalg.norm(X[j] - X[i])**2) *
                                 q[i] * q[j])
                else:
                    FORCE[i] += (((X[i] - X[j]) / np.linalg.norm(X[j] - X[i])**2) * q[i] * q[j])




def move_particles():
    for i in range(POPULATION_SIZE):
        if abs(VALUES[i] - BEST_VALUE) > 1e-3:
            alpha = np.random.uniform()
            velocity = np.ones_like(X[i])
            normalized_force = FORCE[i] / np.linalg.norm(FORCE[i])
            for j in range(N):
                if FORCE[i][j] > 0:
                    velocity[j] = MAX - X[i][j]
                else:
                    velocity[j] = X[i][j] - MIN
            X[i] += alpha * np.multiply(normalized_force, velocity)




def main():
    create_population()
    history = []
    for i in range(MAX_ITER):
        history.append(BEST_VALUE)
        print(f'Текущее лучшее значение: {round(BEST_VALUE, 4)}'
              ' в точке {list(map(lambda x: round(x, 4), best_x))}')
        print(f'Итерация: {i + 1}')
        local_search()
        calculate_force()
        move_particles()




if __name__ == '__main__':
    main()
