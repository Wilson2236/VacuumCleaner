import sys
from area import Area
from basicBot import BasicBot
from statefulBot import *

class DistributedBot(BasicBot):
    minDistanceBetweenBots = 50
    maxDistanceBetweenBots = 200

    def updateCleaningState(self, registryPassives: list, registryActives: list):
        if not self.isInArea(self.state.bounds):
            self.stateToReturn.append(self.state)
            self.state = State(BotStateNames.MovingToTarget, self.state.bounds, self.mapBoundaries)
            return
        target = self.findBestDirt(registryPassives, registryActives)
        if target == None:
            self.state = None
        else:
            self.stateToReturn.append(self.state)
            self.state = State(BotStateNames.MovingToTarget, target, self.state.bounds)

    def findBestDirt(self, registryPassives: list, registryActives: list):
        minMoves = inf
        bestDirt = None
        for rr in registryPassives:
            if isinstance(rr, Dirt) and self.state.bounds.contains(rr):
                moves = self.totalForce(rr, registryActives)
                if moves < minMoves:
                    minMoves = moves
                    bestDirt = rr
        return bestDirt

    def totalForce(self, object: Entity or Point, registryActives: list):
        movesToTarget = self.approximateNumberOfMovesTo(object)
    
        repulsionCoefficient = 0
        for rr in registryActives:
            if isinstance(rr, Bot) and rr != self:
                distanceToBot = object.distanceTo(rr)
                if distanceToBot < sys.float_info.epsilon:
                    repulsionCoefficient = float('inf')
                else:
                    repulsionCoefficient = max(repulsionCoefficient, max(1, DistributedBot.maxDistanceBetweenBots / distanceToBot + sys.float_info.epsilon))
        movesToTarget *= repulsionCoefficient
        if self.priorityArea != None and not self.isInArea(self.priorityArea):
            distanceToPA = self.distanceTo(self.priorityArea)
            distanceFromObjectToPA = object.distanceTo(self.priorityArea)
            attractionCoefficient = max(-1/3, 2/3 - distanceFromObjectToPA / distanceToPA + sys.float_info.epsilon)
            movesToTarget -= (attractionCoefficient * movesToTarget)
        return movesToTarget

    def updateState(self, registryActives: list, registryPassives: list):
        if self.state != None:
            if self.state.name == BotStateNames.MovingToTarget:
                self.updateMovingToTargetState(registryPassives)
            elif self.state.name == BotStateNames.Cleaning:
                self.updateCleaningState(registryPassives, registryActives)
            else:
                self.updateMovingAway(DistributedBot.minDistanceBetweenBots)

        if(self.state == None):
            if(self.stateToReturn):
                if(self.priorityArea != None and self.isInArea(self.priorityArea) and not self.isCleaningArea(self.priorityArea)):
                    self.state = State(BotStateNames.Cleaning, None, self.priorityArea)
                    return
                bots = self.tooCloseBots(registryActives, self.stateToReturn[-1].bounds)
                if bots:
                    self.state = State(BotStateNames.MovingAway, bots, self.stateToReturn[-1].bounds)
                else:
                    self.state = self.stateToReturn.pop()
                    self.updateState(registryActives, registryPassives)

    def tooCloseBots(self, registryActives: list, bounds: Area) -> list:
        if Bot.mapBoundaries.contains(bounds):
            return []
        bots = []
        for rr in registryActives:
            if isinstance(rr, Bot) and rr is not self:
                if self.distanceTo(rr) < DistributedBot.minDistanceBetweenBots:
                    bots.append(rr)
        
        return bots