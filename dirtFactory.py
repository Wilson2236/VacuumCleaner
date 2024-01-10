import random
from tkinter import Canvas

from numpy import ndarray
from dirt import Dirt
from point import Point
from constants import dirtSpotSize
class DirtFactory:
    dirtProduced = 0

    def __init__(self, canvas: Canvas):
        self.canvas = canvas

    def initialiseDirtyFloor(self, map: ndarray, numberOfDirt: int, registryPassives: list):
        if(map.size < numberOfDirt):
            raise Exception("Too many dirt spots for the map size.")
        dirtCreated = 0
        while numberOfDirt > 0:
            registryPassives, map, dirtCreated = self.addDirtSpot(map, registryPassives, numberOfDirt)
            numberOfDirt -= dirtCreated

        return registryPassives, map

    def addDirtSpot(self, map: ndarray, registryPassives: list, dirtLimit = 0):
        dirtSpotCentralPoint = Point(random.randint(dirtSpotSize * 2, map.shape[0] - dirtSpotSize * 2), random.randint(dirtSpotSize * 2, map.shape[0] - dirtSpotSize * 2))
        dirtChance = 0.03
        dirtCreated = 0
        for xx in range(dirtSpotCentralPoint.x - dirtSpotSize, dirtSpotCentralPoint.x + dirtSpotSize):
            for yy in range(dirtSpotCentralPoint.y - dirtSpotSize, dirtSpotCentralPoint.y + dirtSpotSize):
                if not map[xx][yy] and random.random() < dirtChance:
                    map[xx][yy] = 1
                    point = Point(xx, yy)
                    dirt = Dirt("Dirt" + str(DirtFactory.dirtProduced), point)
                    DirtFactory.dirtProduced += 1
                    registryPassives.append(dirt)
                    dirt.draw(self.canvas)
                    dirtCreated += 1
                    if dirtLimit != 0 and dirtCreated == dirtLimit:
                        return registryPassives, map, dirtCreated

        return registryPassives, map, dirtCreated