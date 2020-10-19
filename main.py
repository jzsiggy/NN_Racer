import pyglet
from pyglet.window import Window
from pyglet.window import key
from pyglet import shapes

import math

from Generation import Generation

from track import tracklines

window = Window(960, 700)
pyglet.gl.glClearColor(1,1,1,1)

gen = Generation()

for car in gen.players:
    window.push_handlers(car.key_handler)

@window.event
def on_draw():
    window.clear()
    gen.draw()
    for line in tracklines:
        line.draw()

    # for car in gen.players:  
    #     car.draw()

    # for car in gen.players: 
    #     for line in car.rays:
    #         line.draw()

    # for car in gen.players: 
    #     for intersection in car.intersections:
    #         intersection.draw()

def update(dt):
    gen.update(dt)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/30.0)
    pyglet.app.run()
