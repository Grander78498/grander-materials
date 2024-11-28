import pandas as pd
import numpy as np


def generate(min_coord: int, max_coord: int, min_weight: int, max_weight: int,
             n_places: int):
    coord_x = np.random.randint(min_coord, max_coord, size=(n_places, ))
    coord_y = np.random.randint(min_coord, max_coord, size=(n_places, ))
    weight = np.random.randint(min_weight, max_weight, size=(n_places, ))

    return coord_x, coord_y, weight


def main():
    min_coord, max_coord, min_weight, max_weight, n = -50, 50, 1, 7, 10
    x, y, weight = generate(min_coord, max_coord, min_weight, max_weight, n + 1)
    df = pd.DataFrame({'x': x, 'y': y, 'weight': weight})
    df.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()
