import math
import pyglet
from pyglet.window import key

from shapely.geometry import Point
from shapely.geometry import LineString


from track_points import inner, outer
from Brain import Brain
from assets import center_image

class Player(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_handler = key.KeyStateHandler()
        self.velocity = 0.0
        self.thrust = 300.0
        self.rotate_speed = 100.0
        self.keys = dict(left=False, right=False, up=False, down=False)
        self.rotation = 0.0001
        self.angle_radians = -math.radians(self.rotation)
        
        self.brain = Brain(None)
        self.impulse = [0, 0, 0, 0]

        self.individual = 0
        self.distance_traveled = 0
        self.longest_distance = 0

        self.current_best_network = None
        self.previous_best_network = None

        self.last_ten_ditances = []

        img = pyglet.image.load('bad.png')
        center_image(img)
        self.red = img

        img = pyglet.image.load('car.png')
        center_image(img)
        self.blue = img

    def turn_left(self, dt):
        self.rotation -= self.rotate_speed * dt

    def turn_right(self, dt):
        self.rotation += self.rotate_speed * dt
    
    def brake(self, dt):
        if self.velocity > 0:
            self.velocity -= 3 * self.thrust * dt
            if (self.velocity < 0):
                self.velocity = 0
        else:
            self.velocity = 0
    
    def accelerate(self, dt):
        top = 250
        if self.velocity >= top:
            self.velocity = top
        else:
            self.velocity += self.thrust * dt

    def slow_down(self, dt):
        if self.velocity > 0:
            self.velocity -= self.thrust * dt
        else:
            self.velocity = 0

    # def update_key_pressed(self, dt):
    #     if self.key_handler[key.LEFT]:
    #         self.turn_left(dt)

    #     if self.key_handler[key.RIGHT]:
    #         self.turn_right(dt)
        
    #     if self.key_handler[key.DOWN]:
    #         self.brake(dt)
        
    #     if self.key_handler[key.UP]:
    #         self.accelerate(dt)
    #     else:
    #         self.slow_down(dt)

    def update_impulses(self, dt):
        thresh = 0

        self.accelerate(dt)
        if self.impulse[0] > thresh:
            self.turn_left(dt)

        if self.impulse[1] > thresh:
            self.turn_right(dt)
        
        if self.impulse[2] > thresh:
            self.brake(dt)

    def is_out_of_bounds(self):
        tracklines = []
        for point1, point2 in zip(outer[:-1], outer[1:]):
            line = LineString([
                (point1[0], point1[1]), 
                (point2[0], point2[1])
            ])
            tracklines.append(line)

        for point1, point2 in zip(inner[:-1], inner[1:]):
            line = LineString([
                (point1[0], point1[1]), 
                (point2[0], point2[1])
            ])
            tracklines.append(line)

        position = Point(self.x, self.y)
        current = position.buffer(5).boundary

        for boundry in tracklines:
            i = boundry.intersects(current)
            if i:
                self.image = self.red
                self.reset()
            else:
                self.image = self.blue

    def update_last_ten_distances(self):
        self.last_ten_ditances.append(self.distance_traveled)
        self.last_ten_ditances = self.last_ten_ditances[-10:]

    def check_inplace(self):
        if (len(self.last_ten_ditances) >= 10):
            if (round(self.last_ten_ditances[0]) == round(self.last_ten_ditances[9])):
                self.reset()
                

    def update_distance_traveled(self, dt):
        self.distance_traveled += self.velocity * dt

    def set_impulse(self, impulse):
        # called from Raycaster 
        self.impulse = impulse

    def update(self, dt):
        force_x, force_y = 0.0, 0.0
        self.angle_radians = -math.radians(self.rotation)

        # self.update_key_pressed(dt)
        self.update_impulses(dt)
        self.update_distance_traveled(dt)
        self.update_last_ten_distances()

        force_x = self.velocity * math.cos(self.angle_radians)
        force_y = self.velocity * math.sin(self.angle_radians)

        self.x += force_x * dt
        self.y += force_y * dt

        self.is_out_of_bounds()
        self.check_inplace()

    def reset(self):
        if (self.distance_traveled > self.longest_distance):
            self.longest_distance = self.distance_traveled
            self.current_best_network = self.brain.network
            print('UPDATED BEST')

        self.x = 480
        self.y = 100
        self.velocity = 0.0
        self.rotation = 0.0001
        self.angle_radians = -math.radians(self.rotation)
        self.distance_traveled = 0
        self.impulse = [0, 0, 0, 0]
        self.last_ten_ditances = []
    
        self.individual+=1


        # LEARNING STRATEGY...

        print(self.individual)

        if (self.individual >= 120):
            if (self.individual % 30 == 0):
                print('NEW GEN')
                self.previous_best_network = self.current_best_network
            self.brain = Brain(self.previous_best_network)
        
        else:
            self.brain = Brain(None)

        print(self.brain.network.biases)

