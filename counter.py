from tkinter import Canvas
from area import Area
import constants


class Counter:
    def __init__(self, canvas: Canvas, uncollectedDirtNumber: int, area: Area):
        self.score = 0
        self.canvas = canvas
        self.canvas.create_text(70, 50, text="Score: " + str(self.score), tags="counter")
        self.uncollectedDirtNumber = uncollectedDirtNumber
        self.totalDirtAddedNumber = uncollectedDirtNumber
        self.priorityArea = area
        self.priorityAreaExistedMoves = 0
        self.existanceOfPriorityAreas = 0

    def dirtAdded(self, dirtNumber: int):
        self.uncollectedDirtNumber += dirtNumber
        self.totalDirtAddedNumber += dirtNumber

    def setPriorityArea(self, area: Area):
        self.removePriorityArea()
        self.priorityArea = area
        self.priorityArea.draw(self.canvas, color=constants.priorityZoneColor)
        self.priorityAreaExistedMoves = 0

    def removePriorityArea(self):
        if self.priorityArea == None:
            return 
        self.canvas.delete(self.priorityArea.name)
        self.priorityArea = None
        self.score += (constants.priorityAreaCleanedPoints - self.priorityAreaExistedMoves) # priorityAreaCleanedPoints=500
        # print("Priority area cleaned points:", constants.priorityAreaCleanedPoints) 
        
    def itemCollected(self):
        self.uncollectedDirtNumber -= 1
        self.score += constants.scoreForDirtCollected
        self.canvas.itemconfigure("counter", text="Score: " + str(self.score))

    def movePassed(self):
        if self.priorityArea != None:
            self.priorityAreaExistedMoves += 1
            self.existanceOfPriorityAreas += 1
            # print("Priority area existed moves:", self.priorityAreaExistedMoves)

        
        # print(self.uncollectedDirtNumber * constants.scoreLossPerMove)
        # print(self.score)
        self.score -= (self.uncollectedDirtNumber * constants.scoreLossPerDirt)
        # print(self.score)
        self.canvas.itemconfigure("counter", text=f"Score: %.2f" %self.score)
        self.canvas.delete("priorityAreaCounter")
        # Create a new text object to display existanceOfPriorityAreas
        self.canvas.delete("priorityAreaCounter")
        self.canvas.create_text(70, 70, text=f"Prioritised Areas: {self.existanceOfPriorityAreas}", tags="priorityAreaCounter")
        self.canvas.delete("dirtCounter")
        # Create a new text object to display totalDirtAddedNumber
        self.canvas.create_text(70, 90, text=f"Total Dirt Added: {self.totalDirtAddedNumber}", tags="dirtCounter")
        self.canvas.delete("uncollectedDirtCounter")
        self.canvas.create_text(70, 110, text=f"Uncollected Dirt: {self.uncollectedDirtNumber}", tags="uncollectedDirtCounter")
        