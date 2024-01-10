from tkinter import Canvas
from dirt import Dirt
from entity import Entity
from point import Point
import constants

class Area(Entity):
    def __init__(self, point: Point, width: int, height: int, name = ""):
        super().__init__(point, name)
        self.width = width
        self.height = height
  
    def getOutline(self):
        return [
            Point(self.centralPoint.x - self.width / 2, self.centralPoint.y - self.height / 2),
            Point(self.centralPoint.x - self.width / 2, self.centralPoint.y + self.height / 2),
            Point(self.centralPoint.x + self.width / 2, self.centralPoint.y - self.height / 2),
            Point(self.centralPoint.x + self.width / 2, self.centralPoint.y + self.height / 2),
        ]

    def getBoundaries(self):
        xMin = self.centralPoint.x - self.width / 2
        xMax = self.centralPoint.x + self.width / 2
        yMin = self.centralPoint.y - self.height / 2
        yMax = self.centralPoint.y + self.height / 2

        return xMin, xMax, yMin, yMax

    def contains(self, object: Point or Entity or 'Area') -> bool:
        if isinstance(object, Area):
            for point in object.getOutline():
                if not self.contains(point):
                    return False
            return self.width > object.width and self.height > object.height
        elif isinstance(object, Entity):
            point = object.centralPoint
        else:
            point = object

        if point.x < self.centralPoint.x - self.width / 2 or\
            point.x > self.centralPoint.x + self.width / 2 or \
            point.y < self.centralPoint.y - self.height / 2 or \
            point.y > self.centralPoint.y + self.height / 2:
            return False
        return True

    def isOverlapping(self, area: 'Area') -> bool:
        area1xMin, area1xMax, area1yMin, area1yMax = self.getBoundaries()
        area2xMin, area2xMax, area2yMin, area2yMax = area.getBoundaries()

        if area1xMin < area2xMax and area1xMax > area2xMin and area1yMin < area2yMax and area1yMax > area2yMin:
            return True
        return False

    def getOverlappingArea(self, area: 'Area') -> 'Area':
        if self.contains(area):
            return area
        elif area.contains(self):
            return self
        else:
            area1xMin, area1xMax, area1yMin, area1yMax = self.getBoundaries()
            area2xMin, area2xMax, area2yMin, area2yMax = area.getBoundaries()
            overlappingAreaxMin = max(area1xMin, area2xMin)
            overlappingAreaxMax = min(area1xMax, area2xMax)
            overlappingAreayMin = max(area1yMin, area2yMin)
            overlappingAreayMax = min(area1yMax, area2yMax)

            width = overlappingAreaxMax - overlappingAreaxMin
            height = overlappingAreayMax - overlappingAreayMin

            if width % 2 != 0:
                width += 1
            if height % 2 != 0:
                height += 1
            return Area(Point(overlappingAreaxMin + width / 2,  overlappingAreayMin + height / 2), width, height)
                

    def isClean(self, registryPassives: 'Area') -> bool:
        for rr in registryPassives:
            if isinstance(rr, Dirt):
                if self.contains(rr):
                    return False
        
        return True

    def draw(self, canvas: Canvas, color = "black"):        
        canvas.create_rectangle(self.centralPoint.x - self.width / 2, self.centralPoint.y - self.height / 2, self.centralPoint.x + self.width / 2, self.centralPoint.y + self.height / 2, outline=color,tags=self.name)
