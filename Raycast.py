import pyglet
from pyglet import shapes
import math

class Raycast():
  def __init__(self, car):
    self.update(car)
    self.rays = []
  
  def cast(self, rotation):
    s = math.sin( rotation )
    c = math.cos( rotation )

    line = shapes.Line(
      self.car.x, 
      self.car.y,
      self.car.x + 1000*s,
      self.car.y + 1000*c,
      width=0.5,
    )

    return line

  def cast_rays(self):
    self.rays = []
    for key, rotation in self.directions.items():
       self.rays.append( self.cast(rotation) )

  def update(self, car):
    self.car = car
    self.directions = {
      'front' : self.car.angle_radians,
      'left_diag' : self.car.angle_radians - (math.pi / 4),
      'right_diag' : self.car.angle_radians + (math.pi / 4),
      'left' : self.car.angle_radians - (math.pi / 2),
      'right' : self.car.angle_radians + (math.pi / 2),
    }
    self.cast_rays()
  