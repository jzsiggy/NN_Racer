import pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet.gl import *

import math

from Player import car
from track import track


window = Window(960, 700)
window.push_handlers(car.key_handler)

@window.event
def on_draw():
    window.clear()
    track.draw()
    car.draw()

    # DRAW RAYCASTS
    s = math.sin(car.angle_radians)
    c = math.cos(car.angle_radians)

    glBegin(GL_LINES)
    glVertex2f(car.x,car.y)
    glVertex2f(car.x + 1000*s,car.y + 1000*c)
    glEnd()

def update(dt):
    car.update(dt)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
