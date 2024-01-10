# Class to run experiment for all the different strategy 
import tkinter as tk
import numpy as np
from area import Area
from basicBot import BasicBot
from bot import Bot
from counter import Counter
from dirtFactory import DirtFactory
from distributedBot import DistributedBot
from point import Point
import random
import constants
from statefulBot import StatefulBot
from squaredArea import SquaredArea
from supervisor import Supervisor

class Experiment:
    def initialise(self) -> tk.Canvas:
        self.window.resizable(False,False)
        self.canvas = tk.Canvas(self.window,width=constants.size,height=constants.size)
        self.canvas.pack()
        return self.canvas

    def register(self, initialNumberOfDirt: int, numberOfBots: int):
        self.registryActives = []
        self.registryPassives = []
        self.map = np.zeros( (constants.size, constants.size), dtype=np.int16)
        self.dirtFactory = DirtFactory(self.canvas)
        self.registryPassives, self.map = self.dirtFactory.initialiseDirtyFloor(self.map, initialNumberOfDirt, self.registryPassives)
        
        for i in range(0, numberOfBots):
            bot = self.createBot("Bot" + str(i))
            self.registryActives.append(bot)
            bot.draw(self.canvas)
        self.counter = Counter(self.canvas, initialNumberOfDirt, None)
        self.currentMove = 0
        self.numberOfPriorityAreaCreated = 0

    def createBot(self, botName: str) -> Bot:
        return BasicBot(botName)
    
    def handlePriorityAreaCreation(self, priorityArea: Area):
        self.numberOfPriorityAreaCreated += 1
        for rr in self.registryActives:
            rr.setPriorityArea(priorityArea)

    def handlePriorityAreaRemoval(self):
        for rr in self.registryActives:
            rr.removePriorityArea()

    def choosePriorityArea(self) -> Area:

        return SquaredArea(
            Point(
                random.randint(constants.priorityZoneSize / 2, self.map.shape[0] - constants.priorityZoneSize / 2), 
                random.randint(constants.priorityZoneSize / 2, self.map.shape[0] - constants.priorityZoneSize / 2)
            ),
            constants.priorityZoneSize,
            constants.priorityAreaName
        )

    def moveIt(self, numberOfMoves: int) -> float:
        self.currentMove += 1
        if self.counter.priorityArea != None and (self.counter.priorityArea.isClean(self.registryPassives) or not (self.currentMove % constants.priorityAreaMaxLifeTime)):
            self.counter.removePriorityArea()
            self.handlePriorityAreaRemoval()
        for rr in self.registryActives:
            rr.transferFunction()
            rr.move(self.canvas, 1.0, self.registryActives, self.registryPassives)
            self.registryPassives, self.map = rr.collectDirt(self.canvas, self.registryPassives, self.counter, self.map)
   
        self.counter.movePassed()
        # print(self.currentMove)
        if self.currentMove > numberOfMoves:
            self.window.destroy()
            return

        if not (self.currentMove % 100):
            self.registryPassives, self.map, amountOfDirtAdded = self.dirtFactory.addDirtSpot(self.map, self.registryPassives)
            self.counter.dirtAdded(amountOfDirtAdded)
        if not (self.currentMove % constants.priorityAreaMaxLifeTime):
            priorityArea = self.choosePriorityArea()
            self.counter.setPriorityArea(priorityArea)
            self.handlePriorityAreaCreation(priorityArea)
        
        self.canvas.after(1, self.moveIt, numberOfMoves)

    def run(self, numberOfMoves: int, initialNumberOfDirt: int, numberOFBots: int):
        self.window = tk.Tk()
        self.canvas = self.initialise()
        self.register(initialNumberOfDirt, numberOFBots)
        priorityArea = self.choosePriorityArea()
        priorityArea.draw(self.canvas, constants.priorityZoneColor)
        self.handlePriorityAreaCreation(priorityArea)
        self.counter.setPriorityArea(priorityArea)
        self.moveIt(numberOfMoves)
        self.window.mainloop()
        return self.counter

class ExperimentWithSupervisedSystem(Experiment):
    def register(self, initialNumberOfDirt: int, numberOfBots: int):
        super().register(initialNumberOfDirt, numberOfBots)
        self.supervisor = Supervisor(self.registryActives, constants.size, self.canvas)
    
    def handlePriorityAreaCreation(self, priorityArea: Area):
        self.numberOfPriorityAreaCreated += 1
        self.supervisor.setPriorityArea(priorityArea)

    def handlePriorityAreaRemoval(self):
        self.supervisor.removePriorityArea()

    def createBot(self, botName: str) -> Bot:
        return StatefulBot(botName)

class ExperimentWithDistributedSystem(Experiment):
    def createBot(self, botName: str) -> Bot:
        return DistributedBot(botName)