import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.metrics import accuracy_score


class CPN:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size

        self.weights_kohonen = np.random.rand(input_size, hidden_size)

        self.weights_grossberg = np.random.rand(hidden_size, output_size)

    def train_kohonen(self, data, epochs=100, learning_rate=0.1):
        for epoch in range(epochs):
            for x in data:
                bmu_index = np.argmax(np.dot(x, self.weights_kohonen))
                self.weights_kohonen[:, bmu_index] += learning_rate * (x - self.weights_kohonen[:, bmu_index])

    def train_grossberg(self, data, labels, epochs=100, learning_rate=0.1):
        for epoch in range(epochs):
            print(f'Epoch: {epoch + 1}/{epochs}')
            for x, label in zip(data, labels):
                hidden_output = np.dot(x, self.weights_kohonen)
                hidden_output = hidden_output == np.max(hidden_output)
                hidden_output = hidden_output.astype(int)

                output = np.dot(hidden_output, self.weights_grossberg)

                error = label - output
                self.weights_grossberg += learning_rate * np.outer(hidden_output, error)

    def predict(self, data):
        predictions = []
        for x in data:
            hidden_output = np.dot(x, self.weights_kohonen)
            hidden_output = hidden_output == np.max(hidden_output)
            hidden_output = hidden_output.astype(int)

            output = np.dot(hidden_output, self.weights_grossberg)
            predictions.append(np.argmax(output))
        return np.array(predictions)


def main():
    iris = load_iris()
    X = iris.data
    y = iris.target

    X = (X - X.mean(axis=0)) / X.std(axis=0)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    encoder = OneHotEncoder(sparse_output=False)
    y_train_one_hot = encoder.fit_transform(y_train.reshape(-1, 1))
    y_test_one_hot = encoder.transform(y_test.reshape(-1, 1))

    input_size = X_train.shape[1]
    hidden_size = 10
    output_size = y_train_one_hot.shape[1]
    cpn = CPN(input_size, hidden_size, output_size)
    cpn.train_kohonen(X_train, epochs=100, learning_rate=0.1)
    cpn.train_grossberg(X_train, y_train_one_hot, epochs=100, learning_rate=0.1)

    predictions = cpn.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Точность на тестовом наборе: {accuracy:.2f}")


if __name__ == '__main__':
    main()