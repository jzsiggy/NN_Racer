import pyglet
from pyglet import shapes

import math
import numpy as np

from shapely.geometry import LineString
from shapely.geometry import Point

from track_points import inner, outer
from Player import Player

class Raycaster(Player):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.rays = []
    self.intersections = []
    self.distances = []
    self.tracklines = []
    self.set_track_lines()
  
  def set_track_lines(self):
    for point1, point2 in zip(outer[:-1], outer[1:]):
      line = LineString([
        (point1[0], point1[1]), 
        (point2[0], point2[1])
      ])
      self.tracklines.append(line)

    for point1, point2 in zip(inner[:-1], inner[1:]):
      line = LineString([
        (point1[0], point1[1]), 
        (point2[0], point2[1])
      ])
      self.tracklines.append(line)
  
  def cast(self, rotation):
    s = math.sin( rotation )
    c = math.cos( rotation )

    line = shapes.Line(
      self.x, 
      self.y,
      self.x + 300*c,
      self.y + 300*s,
      color=(0, 255, 0),
      width=0.5,
    )

    return line

  def cast_rays(self):
    self.rays = []
    for name, rotation in self.directions.items():
       self.rays.append( self.cast(rotation) )


  def find_intersection(self, radians):
    s = math.sin( radians )
    c = math.cos( radians )

    l = LineString([
      (self.x, self.y), 
      (self.x + 300*c, self.y + 300*s)
    ])

    intersections = []

    for boundry in self.tracklines:
      i = boundry.intersection(l)
      try:
        (i_x, i_y) = i.x, i.y
        intersections.append((i_x, i_y))
      except:
        i_x, i_y = 0, 0
    
    position = Point(self.x, self.y)
    closest = (0, 0)
    d = 1000

    for entry in intersections:
      point = Point(entry)
      if (position.distance(point) < d):
        d = position.distance(point)
        closest = entry

    circle = shapes.Circle(closest[0], closest[1], 7, color=(255, 0, 0))
    distance = d
    
    return circle, distance

  def get_interesections(self):
    self.intersections = []
    self.distances = []
    for name, radians in self.directions.items():
      intersection, distance = self.find_intersection( radians )
      self.intersections.append(intersection)
      self.distances.append(distance)

  def get_impulse(self):
    features = [*self.distances, self.velocity]
    x = np.array(features)
    super().set_impulse(self.brain.get_impulse(features))

  def update(self, dt):
    super().update(dt)
    self.directions = {
      'front' : self.angle_radians,
      'left_frontal' : self.angle_radians + (math.pi / 8),
      'right_frontal' : self.angle_radians - (math.pi / 8),
      'left_diag' : self.angle_radians + (math.pi / 4),
      'right_diag' : self.angle_radians - (math.pi / 4),
      'left' : self.angle_radians + (math.pi / 2),
      'right' : self.angle_radians - (math.pi / 2),
    }
    self.cast_rays()
    self.get_interesections()
    self.get_impulse()  