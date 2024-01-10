from tkinter import Canvas
from point import Point

class Entity:
    entitiesCreated = 0
    def __init__(self, point: Point, name = ""):
        if not name:
            name = "entity" + str(Entity.entitiesCreated)
        self.centralPoint = point
        Entity.entitiesCreated += 1
        self.name = name

    def angleYaxis(self, object: Point or 'Entity') -> float:
        if isinstance(object, Point):
            return self.centralPoint.angleYaxis(object)
        return self.centralPoint.angleYaxis(object.centralPoint)

    def distanceTo(self, object: Point or 'Entity') -> float:
        if isinstance(object, Point):
            return self.centralPoint.distanceTo(object)
        return self.centralPoint.distanceTo(object.centralPoint)

    def draw(self, canvas: Canvas):
        pass