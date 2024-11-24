import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.cluster import KMeans


class RBFNetwork:

    def __init__(self, input_dim, hidden_dim, output_dim, lr=0.01, epochs=100):
        self.input_dim = input_dim
        self.hidden_dim = hidden_dim
        self.output_dim = output_dim
        self.lr = lr
        self.epochs = epochs

    def init_centers(self, dataset: np.ndarray):
        kmeans = KMeans(n_clusters = self.hidden_dim, random_state = 78498)
        kmeans.fit_predict(dataset)
        self.centers = kmeans.cluster_centers_

    @staticmethod
    def gaussian_rbf(x, center, beta):
        return np.linalg.norm(x - center)

    def compute_rbf_layer(self, X):
        # Рассчитываем радиально-базисные функции для входного слоя
        beta = 1.0  # Параметр ширины RBF
        RBF_output = np.zeros((X.shape[0], self.hidden_dim))
        for i, sample in enumerate(X):
            for j, center in enumerate(self.centers):
                RBF_output[i, j] = self.gaussian_rbf(sample, center, beta)
        return RBF_output

    def fit(self, X, y):
        RBF_output = self.compute_rbf_layer(X)
        self.weights = np.linalg.pinv(RBF_output) @ y

    def forward(self, X):
        # Вычисляем выход RBF слоя и итоговый выход сети
        RBF_output = self.compute_rbf_layer(X)
        output = RBF_output @ self.weights
        return output

    def train(self, dataset: np.ndarray, target: np.ndarray):
        self.init_centers(dataset)
        self.fit(dataset, target)
        predictions = self.forward(dataset)

        predictions = (predictions >= 0.5).astype(np.int8)
        accuracy = (predictions == target).mean() * 100
        print(f'Точность: {accuracy}%')

    def predict(self, X):
        output = self.forward(X)
        return output


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

    rbf_net = RBFNetwork(input_dim=dataset.train_data.shape[1],
                         hidden_dim=10,  # Количество радиально-базисных функций
                         output_dim=1,
                         lr=0.01,
                         epochs=100)

    rbf_net.train(dataset.train_data, dataset.train_target)

    predictions = rbf_net.predict(dataset.test_data)
    predictions = (predictions >= 0.5).astype(np.int8)
    accuracy = (predictions == dataset.test_target).mean() * 100
    print(f"Точность на тестовом наборе: {accuracy}%")


if __name__ == '__main__':
    main()
