from tkinter import Canvas
from statefulBot import BotStateNames, State
from bot import Bot
from area import Area
from point import Point


class Supervisor:
    def __init__(self, bots: list, mapSize: int, canvas: Canvas) -> None:
        self.bots = bots
        self.assignedAreas = self.assignAreas(mapSize, canvas)
        self.giveDefaultOrders()

    
    def giveDefaultOrders(self):
        for bot in self.bots:
            bot.setStateStack(self.getDefaultOrders(bot))

    def getDefaultOrders(self, bot: Bot):
        area = self.assignedAreas[bot]
        return self.getCleaningOrders(area)

    def getCleaningOrders(self, area: Area):
        return [
            State(BotStateNames.Cleaning, None, area),
            State(BotStateNames.MovingToTarget, area, Bot.mapBoundaries)
        ]

    # Assumption that there are only four bots, since experiments are conducted on this number (for simplicity)
    def assignAreas(self, mapSize: int, canvas: Canvas):
        if len(self.bots) == 2:
            width = mapSize * 0.5
            areas = [
                Area(Point(mapSize * 0.25, mapSize * 0.5), width, mapSize),
                Area(Point(mapSize * 0.75, mapSize * 0.5), width, mapSize),
            ]
        elif len(self.bots) == 4:
            width = mapSize * 0.5
            height = mapSize * 0.5
            areas = [
                Area(Point(mapSize * 0.25, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.25, mapSize * 0.75), width, height),
                Area(Point(mapSize * 0.75, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.75, mapSize * 0.75), width, height)
            ]
        elif len(self.bots) == 8:
            width = mapSize * 0.25
            height = mapSize * 0.5
            areas = [
                Area(Point(mapSize * 0.125, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.375, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.625, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.875, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.125, mapSize * 0.75), width, height),
                Area(Point(mapSize * 0.375, mapSize * 0.75), width, height),
                Area(Point(mapSize * 0.625, mapSize * 0.75), width, height),
                Area(Point(mapSize * 0.875, mapSize * 0.75), width, height)
            ]
        elif len(self.bots) == 10:
            width = mapSize * 0.2
            height = mapSize * 0.5
            areas = [
                Area(Point(mapSize * 0.1, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.3, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.5, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.7, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.9, mapSize * 0.25), width, height),
                Area(Point(mapSize * 0.1, mapSize * 0.75), width, height),
                Area(Point(mapSize * 0.3, mapSize * 0.75), width, height),
                Area(Point(mapSize * 0.5, mapSize * 0.75), width, height),
                Area(Point(mapSize * 0.7, mapSize * 0.75), width, height),
                Area(Point(mapSize * 0.9, mapSize * 0.75), width, height),
            ]
        else:
            raise Exception("Unsupported number of bots.")
        
        assignedAreas = {}
        for area in areas:
            area.draw(canvas)
            distances = []
            bots = [bot for bot in self.bots if bot not in assignedAreas]
            for bot in bots:
                distances.append(bot.approximateNumberOfMovesTo(area))
            minDistance = min(distances)
            index = distances.index(minDistance)
            assignedAreas[bots[index]] = area
        return assignedAreas

    def setPriorityArea(self, priorityArea: Area):
        for bot in self.bots:
            area = self.assignedAreas[bot]
            if area.isOverlapping(priorityArea):
                overlappingArea = area.getOverlappingArea(priorityArea)
                defaultOrders = self.getDefaultOrders(bot)
                priorityAreaOrders = self.getCleaningOrders(overlappingArea)
                bot.setStateStack(defaultOrders + priorityAreaOrders)

    def removePriorityArea(self):
        self.giveDefaultOrders()