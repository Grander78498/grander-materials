import numpy as np
import matplotlib.pyplot as plt


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
            self.b = -np.random.random(size=(output_size, ))

    def train(self, dataset: np.ndarray, target: np.ndarray):
        self.dataset = dataset
        self._init_weights(self.dataset.shape[-1], target.shape[-1])

        accuracy_list = []
        for epoch in range(self.epochs):
            print(f"Epoch: {epoch + 1}/{self.epochs}")
            for row, target_value in zip(self.dataset, target):
                result = row @ self.weights + self.b
                result = (result > 0).astype(np.int8)
                for i in range(len(result)):
                    if result[i] != target_value[i]:
                        if result[i] == 0:
                            self.weights[:, i] += self.lr * row
                            self.b[i] += self.lr
                        else:
                            self.weights[:, i] -= self.lr * row
                            self.b[i] -= self.lr
            epoch_result = self.dataset @ self.weights + self.b
            epoch_result = (epoch_result > 0).astype(np.int8)
            accuracy = (epoch_result == target).mean() * 100
            accuracy_list.append(accuracy)

        plt.plot(range(1, self.epochs + 1), accuracy_list)
        plt.show()

    def test(self, data: np.ndarray, target: np.array):
        result = data @ self.weights + self.b
        result = (result > 0).astype(np.int8)
        print(result)
        accuracy = (result == target).mean() * 100
        return accuracy


def main():
    train_data = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    test_data = train_data.copy()
    train_target = np.array([[0, 0, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0]])
    test_target = train_target.copy()

    nn = StupidNeuralNetwork()
    nn.train(train_data, train_target)
    accuracy = nn.test(test_data, test_target)
    print(f'Accuracy: {accuracy:.2f}%')


if __name__ == '__main__':
    main()
