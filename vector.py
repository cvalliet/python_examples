from math import atan, cos, pow, sin, sqrt

class Vector:
    """
       ^
       |        x,y
       +-------o
       |       |
       +-------+---->
     0,0
    """
    def __init__(self):
        self._x, self._y = 0, 0

    def __str__(self):
        return '%0.4f, %0.4f' % (self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def magnitude(self):
        return sqrt(pow(self._x,2) + pow(self._y, 2))

    @property
    def direction(self):
        return atan(self._y / self._x)

    def from_cartesian(self, x, y):
        self._x, self._y = x, y

    def from_polar(self, r, t):
        self._x = r * cos(t)
        self._y = r * sin(t)

    def to_polar(self):
        return sqrt(pow(self._x,2) + pow(self._y, 2)), atan(self._y / self._x)

    def multiply_by(self, a):
        self._x *= a
        self._y *= a

    def rotate(self, angle, origin=(0, 0)):
        offset_x, offset_y = origin
        adjusted_x = self._x - offset_x
        adjusted_y = self._y - offset_y
        cos_rad = cos(angle)
        sin_rad = sin(angle)
        self._x = offset_x + cos_rad * adjusted_x + sin_rad * adjusted_y
        self._y = offset_y + -sin_rad * adjusted_x + cos_rad * adjusted_y
