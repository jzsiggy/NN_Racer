from Network import Network 
import numpy as np

class Brain():
  def __init__(self, network):
    if network:
      self.network = Network([8, 3])
      self.network.weights = network.weights
      self.network.biases = network.biases
      self.network.tweak()
    else:
      self.network = Network([8, 3])

  def get_impulse(self, distances):
    dist = np.array(distances).reshape(8, 1)
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