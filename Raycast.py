import pyglet
from pyglet import shapes
import math

class Raycast():
  def __init__(self, car):
    self.update(car)
    self.rays = []
    self.intersections = []
  
  def cast(self, rotation):
    s = math.sin( rotation )
    c = math.cos( rotation )

    line = shapes.Line(
      self.car.x, 
      self.car.y,
      self.car.x + 1000*c,
      self.car.y + 1000*s,
      width=0.5,
    )

    return line

  def cast_rays(self):
    self.rays = []
    for name, rotation in self.directions.items():
       self.rays.append( self.cast(rotation) )

  def get_y_intersect(self, radians):
    m = math.tan(radians)
    try:
      b = self.car.y - ( m * self.car.x )
    except:
      b = 0

    return m, b

  def find_intersection(self, radians):
    b, d = 1, 0
    a, c = self.get_y_intersect(radians)
    try:
      x = (d - c) / (a - b)
      y = (a * x) + c
    except:
      x, y = 0, 0

    # validar se a intersecção ocoore a frente do carro
    c = math.cos( radians )
    l1x1 = self.car.x
    l1x2 = self.car.x + 1000*c
    l2x1 = 0
    l2x2 = 2000

    if ( (x > max( min(l1x1, l1x2), min(l2x1, l2x2) )) and
         (x < min( max(l1x1, l1x2), max(l2x1, l2x2) )) ):
       pass
    else:
      x, y = 0, 0

    circle = shapes.Circle(x, y, 7, color=(50, 225, 30))
    return circle

  def get_interesections(self):
    self.intersections = []
    for name, radians in self.directions.items():
      self.intersections.append(self.find_intersection( radians ))

  def update(self, car):
    self.car = car
    self.directions = {
      'front' : self.car.angle_radians,
      'left_diag' : self.car.angle_radians + (math.pi / 4),
      'right_diag' : self.car.angle_radians - (math.pi / 4),
      'left' : self.car.angle_radians + (math.pi / 2),
      'right' : self.car.angle_radians - (math.pi / 2),
    }
    self.cast_rays()
    self.get_interesections()
  