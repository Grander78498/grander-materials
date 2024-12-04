import pandas as pd
import numpy as np


def generate(min_coord: int, max_coord: int, n_places: int):
    coord_x = np.random.randint(min_coord, max_coord, size=(n_places, ))
    coord_y = np.random.randint(min_coord, max_coord, size=(n_places, ))
    return coord_x, coord_y


def main():
    min_coord, max_coord, n = -100, 100, 10
    x, y = generate(min_coord, max_coord, n)
    df = pd.DataFrame({'x': x, 'y': y})
    df.to_csv('data.csv', index=False)


if __name__ == '__main__':
    main()
