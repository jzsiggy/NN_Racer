import pyglet
from pyglet import shapes

from track_points import inner, outer

tracklines = []

for point1, point2 in zip(outer[:-1], outer[1:]):
  line = shapes.Line(
      point1[0], 
      point1[1],
      point2[0], 
      point2[1],
      color=(255, 255, 255),
      width=1.5,
    )
  tracklines.append(line)

for point1, point2 in zip(inner[:-1], inner[1:]):
  line = shapes.Line(
      point1[0], 
      point1[1],
      point2[0], 
      point2[1],
      color=(255, 255, 255),
      width=1.5,
    )
  tracklines.append(line)

