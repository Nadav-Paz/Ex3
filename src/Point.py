class Point:

    """
    A representation of a 2D point on a plane
    """

    def __init__(self, x=0.0, y=0.0, coordinate: tuple = None):
        if coordinate:
            self._x = coordinate[0]
            self._y = coordinate[1]
        else:
            self._x = x
            self._y = y

    def __copy__(self):
        return Point(self._x, self._y)

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def set_x(self, x: float):
        self._x = x

    def set_y(self, y: float):
        self._y = y

    def __repr__(self):
        return "%s, %s, 0.0" % (self._x, self._y)

    def __eq__(self, other):
        return float(other.get_x()) == float(self._x) and float(other.get_y()) == float(self._y)

