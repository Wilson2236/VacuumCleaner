from area import Area
from point import Point


class SquaredArea(Area):
    def __init__(self, point: Point, size: int, name):
        super().__init__(point, size, size, name)