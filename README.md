# Neural Network Racer
Teaching an AI how to drive using neural networks and genetic algorithms

![](/resources/GIF.gif)

# How the AI works
The car's actions are determined by a Neural Network. The weights and biases of the network are initialized randomly. At each generation of 50 cars, the car that was able to travel the furthest will have it's network saved, and the following generation will be spawned with networks based on the previous best car's network.

The neural network receives the distances of the car to the track boundries as input alongside the car's velocity. The output indicates what action the car should take.

The possible outputs are:
- Turn left
- Turn right
- Brake

The car defaults to acceleration.

# File Structure

## /Player.py
Stores the code relevant for the car. 
This includes 
- Physics
- Rotation
- Speed & Acceleration
- Generation and performance metrics
- Implementation of a Genetic ALgorithm to improve the weights of the network


## /Raycaster.py
Stores the code relevant for the Raycaster - How the car knows its location relative to the track. 
This includes 
- Intersection between rays and track
- Monitoring distances from car
- Sending these distances to the neural network
- Generation and performance metrics


## /Network.py
Defines a Neural Network
- Constructor to set weights and biases randomly
- Feedforward information
- Method that slightly tweaks a given weight matrix -> useful for our genetic algorithm

## /Brain.py
Implements the Network
- Initializes our network
- Method that returns the output actions

## /track.py & /track_points.py
Defines the coordinates of our track

## /main.py
Instanciates a new Car & draws the track

## /resources
Images and GIFs