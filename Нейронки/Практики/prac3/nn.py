import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from time import sleep

class StupidLayer:
    @staticmethod
    def softmax_deriv(value, input):
        gradient = []
        for row in range(len(value)):
            row_gradient = []
            for i in range(len(value[row])):
                for j in range(len(input[row])):
                    if i == j:
                        row_gradient.append(value[row][i] * (1-input[row][i]))
                    else: 
                        row_gradient.append(-value[row][i]*input[row][j])
            gradient.append(row_gradient)
        return np.array(gradient)

    def __init__(self, size: tuple[int], lr: float = 0.01, activate: str = 'relu'):
        input_size = size[0]
        output_size = size[1]
        self.weights = np.random.random(size=(input_size, output_size)) - 0.5
        self.b = np.random.random(size=(1, output_size)) - 0.5
        self.lr = lr

        activate_func = {'relu': lambda x: np.maximum(0, x),
                         'sigmoid': lambda x: 1 / (1 + np.exp(-x)),
                         'softmax': lambda x: np.exp(x) / np.sum(np.exp(x), axis=0)}
        derivative = {'relu': lambda x: (x > 0).astype(np.int8),
                      'sigmoid': lambda x: x - np.square(x),
                      'softmax': StupidLayer.softmax_deriv}
        self.deriv_func = activate
        self.activate = activate_func[activate]
        self.deriv = derivative[activate]
        self.input: np.ndarray
        self.output: np.ndarray

    def forward(self, data: np.ndarray):
        self.input = data.copy()
        self.output = self.input @ self.weights + self.b
        self.output = self.activate(self.output)
        return self.output

    def back_prop(self, next_loss: np.ndarray) -> np.ndarray:
        if self.deriv_func != 'softmax':
            self.delta = np.multiply(self.deriv(self.output), next_loss)
        else:
            self.delta = self.deriv(self.output, next_loss)
        return self.delta @ self.weights.T

    def calculate_weights(self):
        self.weights -= self.lr * self.input.T @ self.delta
        self.b -= self.lr * self.delta.sum(axis=0)


class StupidNeuralNetwork:

    def __init__(self, epochs=100, batch_size: int | None = None):
        self.layers = []
        self.epochs = epochs
        self.batch_size = batch_size

    def create_layers(self, input_size: int, output_size: int):
        self.layers = [StupidLayer((input_size, 1024), activate='relu'),
                       StupidLayer((1024, 128), activate='relu'),
                       StupidLayer((128, output_size), activate='sigmoid')]

    def forward(self, row: np.ndarray):
        for layer in self.layers:
            row = layer.forward(row)
        return row

    def backward(self, target: np.ndarray, result: np.ndarray):
        loss_deriv = (result - target)
        for layer in reversed(self.layers):
            loss_deriv = layer.back_prop(loss_deriv)

        for layer in self.layers:
            layer.calculate_weights()

    def train(self, dataset: np.ndarray, target: np.ndarray):
        self.create_layers(dataset.shape[1], target.shape[1])

        accuracy_list = []
        epoch_loss_list = []
        self.batch_size = len(dataset) if self.batch_size is None else self.batch_size

        for epoch in range(self.epochs):
            print(f"Эпоха: {epoch + 1}/{self.epochs}")
            epoch_loss = []
            for i in range(0, len(dataset), self.batch_size):
                X_batch = dataset[i:i + self.batch_size]
                y_batch = target[i:i + self.batch_size]

                result = self.forward(X_batch)
                zeroes = np.zeros_like(result)
                zeroes[np.arange(len(result)), result.argmax(1)] = 1
                result = zeroes.copy()
                loss = 0.5 * (np.square(y_batch.toarray() - result)).mean()
                epoch_loss.append(loss)

                self.backward(y_batch, result)

            avg_loss = np.mean(epoch_loss)
            print(f'Ошибка: {avg_loss}')
            epoch_loss_list.append(avg_loss)

            predictions = self.forward(dataset)
            predictions = (predictions == predictions.max()).astype(np.int8)
            accuracy = abs(predictions - target).mean() * 100
            print(f'Точность: {accuracy}%')
            accuracy_list.append(accuracy)

        plt.plot(range(1, self.epochs + 1), accuracy_list)
        plt.title('Точность')
        plt.show()

        plt.plot(range(1, self.epochs + 1), epoch_loss_list)
        plt.title('Ошибка')
        plt.show()

    def fit(self, data: np.ndarray):
        result = self.forward(data)
        result = (result == result.max()).astype(np.int8)
        return result

    def test(self, data: np.ndarray, target: np.ndarray):
        result = self.fit(data)
        accuracy = abs(result - target).mean() * 100
        print(f'Точность на тестовом датасете: {accuracy}%')
        return accuracy


class Dataset:

    def __init__(self) -> None:
        self._max: pd.DataFrame = None
        self._min: pd.DataFrame = None
        self._std: pd.DataFrame = None
        self._mean: pd.DataFrame = None
        self.weights: np.ndarray = None

    def normalize_data(self, df: pd.DataFrame):
        self.train_data = np.vstack(df['audio'].values)
        if self._max is None:
            self._max = self.train_data.max()
        if self._min is None:
            self._min = self.train_data.min()
        if self._std is None:
            self._std = self.train_data.std()
        if self._mean is None:
            self._mean = self.train_data.mean()

        self.train_data = (self.train_data - self._min) / (self._max - self._min)
        # self.df = (self.df > 0.5).astype(np.int8)
        # self.df = (self.df - self._mean) / self._std
        # self.df = (self.df > 0).astype(np.int8)

    def prepare_dataset(self, df: pd.DataFrame):
        enc = OneHotEncoder()
        enc = enc.fit(df.loc[:, ['genre']])
        self.train_target = enc.transform(df.loc[:, ['genre']])
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

    nn = StupidNeuralNetwork(epochs=100, batch_size=1)
    nn.train(dataset.train_data, dataset.train_target)
    nn.test(dataset.test_data, dataset.test_target)


if __name__ == '__main__':
    main()
