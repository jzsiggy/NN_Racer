import pyglet
from pyglet import shapes
import math

from shapely.geometry import LineString
from shapely.geometry import Point

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
      self.car.x + 300*c,
      self.car.y + 300*s,
      color=(0, 255, 0),
      width=0.5,
    )

    return line

  def cast_rays(self):
    self.rays = []
    for name, rotation in self.directions.items():
       self.rays.append( self.cast(rotation) )

  def get_ray_y_intersect(self, radians):
    m = math.tan(radians)
    try:
      b = self.car.y - ( m * self.car.x )
    except:
      b = 0

    return m, b

  def find_intersection(self, radians):
    s = math.sin( radians )
    c = math.cos( radians )

    p = Point(480, 350)
    b1 = p.buffer(300).boundary
    b2 = p.buffer(250).boundary

    l = LineString([
      (self.car.x - 3000*c, self.car.y - 3000*s), 
      (self.car.x + 3000*c, self.car.y + 3000*s)
    ])
    i1 = b1.intersection(l)
    i2 = b2.intersection(l)

    try:
      (inner_x1, inner_y1) = i2.geoms[1].coords[0]
    except:
      inner_x1, inner_y1 = 0, 0
      
    try:
      (inner_x2, inner_y2) = i2.geoms[0].coords[0]
    except:
      inner_x2, inner_y2 = 0, 0

    try:
      (outer_x1, outer_y1) = i1.geoms[1].coords[0]
    except:
      outer_x1, outer_y1 = 0, 0
      
    try:
      (outer_x2, outer_y2) = i1.geoms[0].coords[0]
    except:
      outer_x2, outer_y2 = 0, 0

    constraint = LineString([
      (self.car.x, self.car.y), 
      (self.car.x + 300*c, self.car.y + 300*s)
    ])
    
    test = [
      (inner_x1, inner_y1),
      (inner_x2, inner_y2),
      (outer_x1, outer_y1),
      (outer_x2, outer_y2)
    ]

    position = Point(self.car.x, self.car.y)
    closest = (0, 0)
    d = math.inf

    for entry in test:
      point = Point(entry)

      if (constraint.distance(point) < 1e-8):
        if (position.distance(point) < d):
          d = position.distance(point)
          closest = entry

    circle = shapes.Circle(closest[0], closest[1], 7, color=(255, 0, 0))
    
    return circle

  def get_interesections(self):
    self.intersections = []
    for name, radians in self.directions.items():
      intersection = self.find_intersection( radians )
      self.intersections.append(intersection)

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
  