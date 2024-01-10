import math

class Point:

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def distanceTo(self, point: 'Point') -> float:
        return self.distanceBetween(self, point)

    def angleYaxis(self, point: 'Point') -> float:
        return self.angleYaxisBetween2Points(self, point)

    @staticmethod
    def distanceBetween(point1: 'Point', point2: 'Point') -> float:
        return math.sqrt( math.pow(point1.x - point2.x, 2) + math.pow(point1.y - point2.y, 2))

    @staticmethod
    def angleYaxisBetween2Points(point1: 'Point', point2: 'Point') -> float:
        deltaX = point2.x - point1.x
        deltaY = point2.y - point1.y

        return math.atan2(deltaY, deltaX) % (2.0 * math.pi)