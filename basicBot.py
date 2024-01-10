from statefulBot import *

class BasicBot(StatefulBot):
    def __init__(self, namep: str):
        super().__init__(namep, [State(BotStateNames.Cleaning, None, Bot.mapBoundaries)])
        self.priorityArea = None

    def setPriorityArea(self, priorityArea: Area):
        self.removePriorityArea()
        self.priorityArea = priorityArea

    def removePriorityArea(self):
        if self.priorityArea != None:
            if self.isCleaningArea(self.priorityArea):
                self.setStateStack([State(BotStateNames.Cleaning, None, Bot.mapBoundaries)])
            self.priorityArea = None

    def isCleaningArea(self, area: Area):
        states = self.stateToReturn
        if self.state != None:
            states.append(self.state)
        for idx, state in enumerate(states):
            if state.name == BotStateNames.Cleaning and state.bounds.name == area.name:
                return True
        return False

    def clean(self):
        if self.state.target == None:
            return
        self.chooseDirectionToTarget()

    def updateState(self, registryActives: list, registryPassives: list):
        if self.state != None:
            if self.state.name == BotStateNames.MovingToTarget:
                self.updateMovingToTargetState(registryPassives)
            elif self.state.name == BotStateNames.Cleaning:
                self.updateCleaningState(registryPassives)
            else:
                self.updateMovingAway()

        if(self.state == None):
            if(self.stateToReturn):
                if(self.priorityArea != None and self.isInArea(self.priorityArea) and not self.isCleaningArea(self.priorityArea)):
                    self.state = State(BotStateNames.Cleaning, None, self.priorityArea)
                    return
                self.state = self.stateToReturn.pop()
                self.updateState(registryActives, registryPassives)