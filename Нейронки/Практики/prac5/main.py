import numpy as np
import matplotlib.pyplot as plt
from minisom import MiniSom

# Генерация синтетических данных
np.random.seed(10)
data = np.random.rand(1000, 2)  # 1000 точек в 2D пространстве

# Инициализация SOM
som_shape = (10, 10)  # Размер карты (10x10)
som = MiniSom(som_shape[0], som_shape[1], data.shape[1], sigma=0.3, learning_rate=0.5)

# Инициализация весов случайными значениями
som.random_weights_init(data)

# Обучение SOM
som.train_random(data, 100)  # Обучение на 100 итераций

# Визуализация результатов
plt.figure(figsize=(7, 7))
for position, vector in zip(som.win_map(data), data):
    plt.text(position[0]+.5, position[1]+.5, '.', color=plt.cm.Reds(vector[0]), fontdict={'weight': 'bold', 'size': 11})
plt.pcolor(som.distance_map().T, cmap='bone_r', alpha=0.2)
plt.colorbar()

plt.show()