import pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet import shapes

import math

from Raycaster import Raycaster
from track import tracklines
from assets import center_image

img = pyglet.image.load('resources/car.png')
center_image(img)
car = Raycaster(img, x=480, y=100)
car.scale = 0.07

window = Window(960, 700)
pyglet.gl.glClearColor(1,1,1,1)
window.push_handlers(car.key_handler)

@window.event
def on_draw():
    window.clear()
    car.draw()

    for line in tracklines:
        line.draw()

    for line in car.rays:
        line.draw()
    
    for intersection in car.intersections:
        intersection.draw()

def update(dt):
    car.update(dt)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/70.0)
    pyglet.app.run()
