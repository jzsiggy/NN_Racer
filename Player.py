import math
import pyglet
from pyglet.window import key

from shapely.geometry import Point

from Brain import Brain
from assets import center_image

class Player(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.key_handler = key.KeyStateHandler()
        self.velocity = 0.0
        self.thrust = 3000.0
        self.rotate_speed = 100.0
        self.keys = dict(left=False, right=False, up=False, down=False)
        self.rotation = 0.0001
        self.angle_radians = -math.radians(self.rotation)
        
        self.individual = 0
        self.distance_traveled = 0
        self.longest_distance = 0
        self.best_network = None

        self.last_ten_ditances = []

        self.brain = Brain(None)
        self.impulse = [0, 0, 0, 0]

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
        else:
            self.velocity = 0
    
    def accelerate(self, dt):
        self.velocity += self.thrust * dt

    def slow_down(self, dt):
        if self.velocity > 0:
                self.velocity -= self.thrust * dt
        else:
            self.velocity = 0

    def update_key_pressed(self, dt):
        if self.key_handler[key.LEFT]:
            self.turn_left(dt)

        if self.key_handler[key.RIGHT]:
            self.turn_right(dt)
        
        if self.key_handler[key.DOWN]:
            self.brake(dt)
        
        if self.key_handler[key.UP]:
            self.accelerate(dt)
        else:
            self.slow_down(dt)

    def update_impulses(self, dt):
        thresh = 0
        if self.impulse[0] > thresh:
            self.turn_left(dt)

        if self.impulse[1] > thresh:
            self.turn_right(dt)
        
        if self.impulse[2] > thresh:
            self.brake(dt)
        
        if self.impulse[3] > thresh:
            self.accelerate(dt)
        # else:
        #     self.slow_down(dt)

    def is_out_of_bounds(self):
        center = Point(480, 350)
        outer = center.buffer(320).boundary
        inner = center.buffer(250).boundary

        position = Point(self.x, self.y)
        current = position.buffer(5).boundary

        i = inner.intersects(current) or outer.intersects(current)
        if i:
            self.image = self.red
            self.reset()
        else:
            self.image = self.blue
        return i

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

        self.update_key_pressed(dt)
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
            self.best_network = self.brain.network
            print('UPDATED BEST')

        self.x = 480
        self.y = 80
        self.velocity = 0.0
        self.rotation = 0.0001
        self.angle_radians = -math.radians(self.rotation)
        self.distance_traveled = 0
        self.impulse = [0, 0, 0, 0]
        self.last_ten_ditances = []
    
        self.individual+=1

        if (self.individual % 20 == 0):
            self.brain = Brain(self.best_network)
            print('NEW GEN')
        else:
            self.brain = Brain(None)

