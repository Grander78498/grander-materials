import numpy as np
import matplotlib.pyplot as plt


def rastrigin(x: np.ndarray):
    return np.sum(x**2 - 10 * np.cos(2 * np.pi * x) + 10)