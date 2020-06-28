import pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet import shapes

import math

from Player import Player
from Raycast import Raycast
from track import track
from assets import center_image


img = pyglet.image.load('car.png')
center_image(img)
car = Player(img, x=480, y=75)
car.scale = 0.07

raycast = Raycast(car)

window = Window(960, 700)
window.push_handlers(car.key_handler)

@window.event
def on_draw():
    window.clear()
    track.draw()
    car.draw()

    for line in raycast.rays:
        line.draw()
    
    for intersection in raycast.intersections:
        intersection.draw()

def update(dt):
    car.update(dt)
    raycast.update(car)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
