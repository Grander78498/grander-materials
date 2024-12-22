import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from tqdm import tqdm
import matplotlib.pyplot as plt


class SOM:
    def __init__(self, map_size, input_size, sigma=0.3, learning_rate=0.5):
        self.map_size = map_size
        self.input_size = input_size
        self.sigma = sigma
        self.learning_rate = learning_rate
        self.weights = np.random.rand(map_size[0], map_size[1], input_size)

    def find_bmu(self, x):
        distances = np.linalg.norm(self.weights - x, axis=2)
        return np.unravel_index(np.argmin(distances), distances.shape)

    def neighborhood_function(self, bmu, iteration):
        t1 = 1000
        t2 = 1000
        sigma_t = self.sigma * np.exp(-iteration / t1)
        learning_rate_t = self.learning_rate * np.exp(-iteration / t2)
        dist_sq = np.sum((np.indices(self.map_size).T - np.array(bmu)).T ** 2, axis=0)
        return learning_rate_t * np.exp(-dist_sq / (2 * sigma_t ** 2))

    def train(self, data, iterations):
        """ Обучение SOM """
        for iteration in tqdm(range(iterations)):
            for x in data:
                bmu = self.find_bmu(x)
                nh_func = self.neighborhood_function(bmu, iteration)
                self.weights += nh_func[:, :, np.newaxis] * (x - self.weights)

    def visualize(self, data):
        plt.figure(figsize=(7, 7))
        plt.pcolor(np.linalg.norm(self.weights, axis=2).T, cmap='bone_r', alpha=0.2)
        plt.colorbar()

        for x in data:
            bmu = self.find_bmu(x)
            plt.text(bmu[1] + 0.5, bmu[0] + 0.5, '.', color=plt.cm.Reds(x[0]), fontdict={'weight': 'bold', 'size': 11})

        plt.show()

    
class Dataset:
    def __init__(self):
        self._max = None
        self._min = None

    def normalize_data(self, df):
        if self._max is None:
            self._max = df.max()
        if self._min is None:
            self._min = df.min()

        self.df = (df - self._min) / (self._max - self._min)

    def prepare_dataset(self):
        self.train_target = self.df['output'].to_numpy().reshape((-1, 1))
        self.train_data = self.df.drop(columns=['output']).to_numpy()
        self.train_data, self.test_data, self.train_target, self.test_target = train_test_split(
            self.train_data,
            self.train_target,
            shuffle=True,
            random_state=78498,
            test_size=0.2
        )


def main():
    df = pd.read_csv('../dataset/heart.csv')
    dataset = Dataset()
    dataset.normalize_data(df)
    dataset.prepare_dataset()
    som_shape = (10, 10)
    som = SOM(som_shape, dataset.train_data.shape[1], sigma=0.3, learning_rate=0.5)
    som.train(dataset.train_data, 100)
    som.visualize(dataset.train_data)


if __name__ == '__main__':
    main()