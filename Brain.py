from Network import Network 
import numpy as np
import random

class Brain():
  def __init__(self):
    self.network = Network([10, 12, 3])

  def breed(self, net1, net2):
    print('breeding')

    for l_index, layer in enumerate(self.network.weights[0]):
      for w_index, weight in enumerate(layer):
        if ( random.choice((True, False)) ):
          self.network.weights[0][l_index][w_index] = net1.weights[0][l_index][w_index]
        else:
          self.network.weights[0][l_index][w_index] = net2.weights[0][l_index][w_index]

    for l_index, layer in enumerate(self.network.weights[1]):
      for w_index, weight in enumerate(layer):
        if ( random.choice((True, False)) ):
          self.network.weights[1][l_index][w_index] = net1.weights[1][l_index][w_index]
        else:
          self.network.weights[1][l_index][w_index] = net2.weights[1][l_index][w_index]

    self.network.tweak()

  def get_impulse(self, distances):
    dist = np.array(distances).reshape(10, 1)
    return self.network.feedforward(dist)

# import numpy as np

# import tensorflow as tf
# from tensorflow import keras

# tf.random.set_seed(2)

# class Brain():
#   def __init__(self):
#     self.network = keras.models.Sequential([
#       keras.layers.Dense(5, input_dim=5, activation='relu'),
#       keras.layers.Dense(4, activation='softmax')
#     ])
#     self.network.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
  
#   def get_impulse(self, distances):
#     dist = np.array([distances])
#     return self.network.predict(dist)