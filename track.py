import pyglet
from pyglet import shapes

track = pyglet.graphics.Batch()

circle = shapes.Circle(480, 350, 320, color=(255, 255, 255), batch=track)
circle_inner = shapes.Circle(480, 350, 250, color=(0, 0, 0), batch=track)

