import pyglet
from pyglet import shapes

track = pyglet.graphics.Batch()

line2 = shapes.Line(0, 0, 2000, 2000, width=4, color=(200, 20, 20), batch=track)