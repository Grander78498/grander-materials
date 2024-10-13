import pandas as pd
import numpy as np


def generate(min_coord: int, max_coord: int, min_weight: int, max_weight: int,
             n_places: int):
    coord_x = np.random.randint(min_coord, max_coord, size=(n_places, ))
    coord_y = np.random.randint(min_coord, max_coord, size=(n_places, ))
    weight = np.random.random(size=(n_places, )) * (max_weight -
                                                    min_weight) + min_weight
    weight = weight.round(2)

    return coord_x, coord_y, weight


def main():
    min_coord, max_coord, min_weight, max_weight, n = -1000, 1000, 0.01, 5, 100
    x, y, weight = generate(min_coord, max_coord, min_weight, max_weight, n)
    df = pd.DataFrame({'x': x, 'y': y, 'weight': weight})
    df.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()
