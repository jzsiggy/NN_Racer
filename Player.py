import math
import pyglet

from shapely.geometry import Point

from pyglet.window import key

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

    def update_key_pressed(self, dt):
        if self.key_handler[key.LEFT]:
            self.rotation -= self.rotate_speed * dt

        if self.key_handler[key.RIGHT]:
            self.rotation += self.rotate_speed * dt
       
        if self.key_handler[key.UP]:
            self.velocity += self.thrust * dt
        else:
            if self.velocity > 0:
                  self.velocity -= self.thrust * dt
            else:
                self.velocity = 0
        
        if self.key_handler[key.DOWN]:
            if self.velocity > 0:
                self.velocity -= 3 * self.thrust * dt
            else:
                self.velocity = 0

    def is_out_of_bounds(self):
        center = Point(480, 350)
        outer = center.buffer(300).boundary
        inner = center.buffer(250).boundary

        position = Point(self.x, self.y)
        current = position.buffer(5).boundary

        i = inner.intersects(current) or outer.intersects(current)
        return i

    def update(self, dt):
        force_x, force_y = 0.0, 0.0
        self.angle_radians = -math.radians(self.rotation)

        self.update_key_pressed(dt)

        force_x = self.velocity * math.cos(self.angle_radians)
        force_y = self.velocity * math.sin(self.angle_radians)

        self.x += force_x * dt
        self.y += force_y * dt

        self.is_out_of_bounds()
