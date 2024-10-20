import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


class StupidLayer:
    def __init__(self, size: tuple[int], lr: float = 0.5, epochs: int = 100, activate: str = 'relu'):
        input_size = size[0]
        output_size = size[1]
        self.weights = np.random.random(size=(input_size, output_size))
        self.b = np.random.random(size=(output_size, ))
        self.lr = lr
        self.epochs = epochs

        activate_func = {'relu': lambda x: np.maximum(np.zeros_like(x), x),
                         'sigmoid': lambda x: 1 / (1 + np.exp(-x))}
        derivative = {'relu': lambda x: (x > 0).astype(np.int8),
                      'sigmoid': lambda x: x * (1 - x)}
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
        print(self.output.shape, next_loss.shape)
        self.delta = self.deriv(self.output).T @ next_loss
        return self.delta
  
    def calculate_weights(self):
        self.weights += self.lr * (self.input.T @ self.delta)
        self.b += self.lr * self.delta.mean(axis=0)


class StupidNeuralNetwork:

    def __init__(self):
        self.layers: list[StupidLayer] | None = None
        self.epochs = 100

    def create_layers(self, input_size: int, output_size: int):
        self.layers = [StupidLayer((input_size, 4), activate='sigmoid'),
                       StupidLayer((4, output_size), activate='sigmoid')]
        
    def forward(self, row: np.ndarray):
        for layer in self.layers:
            row = layer.forward(row)
        return row
    
    def backward(self, target: np.ndarray, result: np.ndarray):
        loss = 1 / 2 * ((target - result) ** 2).sum()
        loss_deriv = (result - target)
        for layer in self.layers[::-1]:
            next_delta = layer.back_prop(loss_deriv)
            print(next_delta.shape)
            loss_deriv = layer.weights * next_delta
            print(loss_deriv.shape)

        for layer in self.layers:
            layer.calculate_weights()
        
        return loss

    def train(self, dataset: np.ndarray, target: np.ndarray):
        self.dataset = dataset

        self.create_layers(self.dataset.shape[-1], target.shape[-1])

        accuracy_list = []
        epoch_list = []
        batch_size = len(target)
        for epoch in range(self.epochs):
            print(f"Epoch: {epoch + 1}/{self.epochs}")
            epoch_loss = []
            for row, target_value in zip(np.split(self.dataset, self.dataset.shape[0] // batch_size),
                                         np.split(target, target.shape[0] // batch_size)):
                result = self.forward(row.copy())
                loss = self.backward(target_value, result)
                epoch_loss.append(loss)
            epoch_loss = np.array(epoch_loss).sum()
            print(f'Loss: {epoch_loss}')
            epoch_list.append(epoch_loss)
            epoch_result = self.forward(self.dataset)
            epoch_result = (epoch_result >= 0.5).astype(np.int8)
            accuracy = (epoch_result == target).mean() * 100
            accuracy_list.append(accuracy)

        plt.plot(range(1, self.epochs + 1), accuracy_list)
        plt.plot(range(1, self.epochs + 1), epoch_list)
        plt.show()

    def test(self, data: np.ndarray, target: np.array):
        result = self.forward(data)
        result = (result >= 0.5).astype(np.int8)
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
        # self.df = (self.df > 0.5).astype(np.int8)
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
    df = pd.read_csv('dataset/heart.csv')
    dataset = Dataset()
    dataset.normalize_data(df)
    dataset.prepare_dataset()

    nn = StupidNeuralNetwork()
    nn.train(dataset.train_data, dataset.train_target)
    accuracy = nn.test(dataset.test_data, dataset.test_target)
    print(f'Accuracy: {accuracy}%')


if __name__ == '__main__':
    main()
