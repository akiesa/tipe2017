import math
import itertools

class Point:
        def __init__(self, x=0.0, y=0.0):
                self.x = x
                self.y = y

        def __add__(self, p):
                """Point(x1+x2, y1+y2)"""
                return Point(self.x+p.x, self.y+p.y)

        def __sub__(self, p):
                """Point(x1-x2, y1-y2)"""
                return Point(self.x-p.x, self.y-p.y)

        def __mul__( self, scalar ):
                """Point(x1*x2, y1*y2)"""
                return Point(self.x*scalar, self.y*scalar)
        def __div__(self, scalar):
                """Point(x1/x2, y1/y2)"""
                return Point(self.x/scalar, self.y/scalar)
        def __str__(self):
                return "(%s, %s)" % (self.x, self.y)
        def __repr__(self):
                return "%s(%r, %r)" % (self.__class__.__name__, self.x, self.y)

        def length(self):
                return math.sqrt(self.x**2 + self.y**2)

        def distance_to(self, p):
                """Calculate the distance between two points."""
                return (self - p).length()
        def as_tuple(self):
                """(x, y)"""
                return (self.x, self.y)

        def clone(self):
                """Return a full copy of this point."""
                return Point(self.x, self.y)

        def integerize(self):
                """Convert co-ordinate values to integers."""
                self.x = int(self.x)
                self.y = int(self.y)

        def floatize(self):
                """Convert co-ordinate values to floats."""
                self.x = float(self.x)
                self.y = float(self.y)

        def move_to(self, x, y):
                """Reset x & y coordinates."""
                self.x = x
                self.y = y

        def slide(self, p):
                self.x = self.x + p.x
                self.y = self.y + p.y

        def slide_xy(self, dx, dy):
                self.x = self.x + dx
                self.y = self.y + dy

        def rotate(self, rad):
                s, c = [f(rad) for f in (math.sin, math.cos)]
                x, y = (c*self.x - s*self.y, s*self.x + c*self.y)
                return Point(x,y)

        def rotate_about(self, p, theta):
                result = self.clone()
                result.slide(-p.x, -p.y)
                result.rotate(theta)
                result.slide(p.x, p.y)
                return result
class Rect:
        def __init__(self, pt1, pt2):
                self.set_points(pt1, pt2)
        def set_points(self, pt1, pt2):
          (x1, y1) = pt1
          (x2, y2) = pt2
          self.left = min(x1, x2)
          self.top = min(y1, y2)
          self.right = max(x1, x2)
          self.bottom = max(y1, y2)

        def width(self):
          return abs(self.right-self.left)

        def height(self):
          return abs(self.top-self.bottom)
  
        def contains(self, pt):
          """Return true if a point is inside the rectangle."""
          x,y = pt
          return (self.left <= x <= self.right and
                  self.top <= y <= self.bottom) 
  
        def overlaps(self, other):
          """Return true if a rectangle overlaps this rectangle."""
          return (self.right > other.left and self.left < other.right and
                 self.top < other.bottom and self.bottom > other.top)
      
        def top_left(self):
          """Return the top-left corner as a Point."""
          return Point(self.left, self.top)
      
        def bottom_right(self):
          """Return the bottom-right corner as a Point."""
          return Point(self.right, self.bottom)
      
        def expanded_by(self, n):
          """Return a rectangle with extended borders.
  
          Create a new rectangle that is wider and taller than the
          immediate one. All sides are extended by "n" points.
          """
          p1 = Point(self.left-n, self.top-n)
          p2 = Point(self.right+n, self.bottom+n)
          return Rect(p1, p2)
      
        def __str__( self ):
          return "<Rect (%s,%s)-(%s,%s)>" % (self.left,self.top,
                                             self.right,self.bottom)
      
        def __repr__(self):
          return "%s(%r, %r)" % (self.__class__.__name__,
                                 Point(self.left, self.top),
                                 Point(self.right, self.bottom))

class GeometricUtils:

  def calculateLongestDistance(pointsList):
    max=((), 0.0)
    for couple in itertools.combinations(pointsList,2):
      pt1=Point(couple[0][0], couple[0][1])
      pt2=Point(couple[1][0], couple[1][1])
      distance=pt1.distance_to(pt2)
      if(distance>max[1]):
        max=((pt1.as_tuple(), pt2.as_tuple()), distance)

    return max[0]

