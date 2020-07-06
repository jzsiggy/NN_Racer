"""
  Network constructor and feedforward method 'borrowed' from mnielsen
"""

import random
import numpy as np

def sigmoid(z):
    return 1.0/(1.0+np.exp(-z))

def relu(z):
  return z * (z > 0)

class Network(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x)
                        for x, y in zip(sizes[:-1], sizes[1:])]

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = relu(np.dot(w, a)+b)
        return a

    def tweak(self):
        print('tweaking')
        d_biases = [np.random.randn(y, 1) * 0.3 for y in self.sizes[1:]]
        d_weights = [np.random.randn(y, x) * 0.3
                        for x, y in zip(self.sizes[:-1], self.sizes[1:])]

        self.weights = np.add(self.weights, d_weights, dtype=object)
        self.biases = np.add(self.biases,d_biases, dtype=object)
