import numpy as np


class Layer:
    def __init__(self, color, max_x, max_y):
        self.color = color
        self.data = np.zeros((max_y, max_x))

