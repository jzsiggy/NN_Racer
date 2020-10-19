import copy
import math
import pyglet
from Brain import Brain
from Raycaster import Raycaster
from assets import center_image

img = pyglet.image.load('resources/car.png')
center_image(img)

class Generation():
    def __init__(self, size=30):
        self.size = size
        self.batch = pyglet.graphics.Batch()
        self.players = [ Raycaster(img, x=480, y=100, batch=self.batch) for player in range(self.size) ]
        self.rescale()

        self.new_best_networks = [
            {
                'distance': 0,
                'network': None
            },
            {
                'distance': 0,
                'network': None
            }
        ]

        self.current_best_networks = [
            {
                'distance': 0,
                'network': None
            },
            {
                'distance': 0,
                'network': None
            }
        ]
    
    def rescale(self):
        for car in self.players:
            car.scale = 0.07

    def check_end_of_gen(self):
        for car in self.players:
            if not car.off:
                return False
        return True
    
    def update(self, dt):
        for car in self.players:
            car.update(dt)
        
        if self.check_end_of_gen():
            print('end')
            self.reset()

    def reset(self):
        self.check_best()
        self.current_best_networks = copy.deepcopy(self.new_best_networks)

        best1 = self.current_best_networks[0]['network']
        best2 = self.current_best_networks[1]['network']
        
        for car in self.players:
            car.brain = Brain()
            car.brain.breed(best1, best2)
            car.angle_radians = -math.radians(car.rotation)
            car.distance_traveled = 0
            car.impulse = [0, 0, 0]
            car.last_ten_ditances = []

            car.x = 480
            car.y = 100
            
            car.rotation = 0.0001
            car.off = False

    def check_best(self):
        current_first = self.current_best_networks[0]
        current_second = self.current_best_networks[1]
        new_first = self.new_best_networks[0]
        new_second = self.new_best_networks[1]

        for car in self.players:
            if (car.distance_traveled > current_first['distance'] and car.distance_traveled > new_first['distance']):
                self.new_best_networks[0]['distance'] = car.distance_traveled
                self.new_best_networks[0]['network'] = car.brain.network
                print('UPDATED BEST')
            elif (car.distance_traveled > current_second['distance'] and car.distance_traveled > new_second['distance']):
                self.new_best_networks[1]['distance'] = car.distance_traveled
                self.new_best_networks[1]['network'] = car.brain.network
                print('UPDATED SECOND BEST')

    def draw(self):
        self.batch.draw()
