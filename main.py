import pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet import shapes

import math

from Player import car
from Raycast import Raycast
from track import track

raycast = Raycast(car)

window = Window(960, 700)
window.push_handlers(car.key_handler)

@window.event
def on_draw():
    window.clear()
    car.draw()
    track.draw()

    for line in raycast.rays:
        line.draw()

def update(dt):
    car.update(dt)
    raycast.update(car)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
