import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


class StupidNeuralNetwork:

    def __init__(self):
        self.weights: np.ndarray = None
        self.b: np.ndarray = None
        self.lr = 0.01
        self.epochs = 100

    def _init_weights(self, input_size: int, output_size: int):
        if self.weights is None:
            self.weights = np.random.random(size=(input_size, output_size))
        if self.b is None:
            self.b = -np.random.random(size=(output_size, 1))

    def train(self, dataset: np.ndarray, target: np.ndarray):
        self.dataset = dataset

        self._init_weights(self.dataset.shape[-1], target.shape[-1])

        accuracy_list = []
        batch_size = len(target)
        for epoch in range(self.epochs):
            print(f"Epoch: {epoch + 1}/{self.epochs}")
            for row, target_value in zip(np.split(self.dataset, self.dataset.shape[0] // batch_size),
                                         np.split(target, target.shape[0] // batch_size)):
                result = row @ self.weights + self.b
                result = (result > 0).astype(np.int8)

                loss = target_value - result
                self.weights += self.lr * (row.T @ loss)
                self.b += self.lr * loss.mean(axis=0)
            epoch_result = self.dataset @ self.weights + self.b
            epoch_result = (epoch_result > 0).astype(np.int8)
            accuracy = (epoch_result == target).mean() * 100
            accuracy_list.append(accuracy)

        plt.plot(range(1, self.epochs + 1), accuracy_list)
        plt.show()

    def test(self, data: np.ndarray, target: np.array):
        result = data @ self.weights + self.b
        result = (result > 0).astype(np.int8).reshape(-1)
        print(result)
        accuracy = (result == target).mean() * 100
        return accuracy


class Dataset:

    def __init__(self) -> None:
        self._max: pd.DataFrame = None
        self._min: pd.DataFrame = None
        self._std: pd.DataFrame = None
        self._mean: pd.DataFrame = None
        self.weights: np.ndarray = None

    def normalize_data(self, df: pd.DataFrame):
        self.df = df
        if self._max is None:
            self._max = self.df.max()
        if self._min is None:
            self._min = self.df.min()
        if self._std is None:
            self._std = self.df.std()
        if self._mean is None:
            self._mean = self.df.mean()

        self.df = (self.df - self._min) / (self._max - self._min)
        self.df = (self.df > 0.5).astype(np.int8)
        # self.df = (self.df - self._mean) / self._std
        # self.df = (self.df > 0).astype(np.int8)

    def prepare_dataset(self):
        self.train_target = self.df['output'].to_numpy().reshape((-1, 1))
        self.train_data = self.df.drop(columns=['output']).to_numpy()
        self.train_data, self.test_data, self.train_target, self.test_target = (
            train_test_split(self.train_data,
                             self.train_target,
                             shuffle=True,
                             random_state=78498,
                             test_size=0.2))


def main():
    df = pd.read_csv('../dataset/heart.csv')
    dataset = Dataset()
    dataset.normalize_data(df)
    dataset.prepare_dataset()

    nn = StupidNeuralNetwork()
    nn.train(dataset.train_data, dataset.train_target)
    accuracy = nn.test(dataset.test_data, dataset.test_target)
    print(f'Accuracy: {accuracy}%')


if __name__ == '__main__':
    main()
