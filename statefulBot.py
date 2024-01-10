from cmath import inf
from tkinter import Canvas
from bot import Bot
from dirt import Dirt
from entity import Entity
from point import Point
from area import Area
import math
from enum import Enum
from geometry import *

class BotStateNames(Enum):
    MovingToTarget = 1,
    MovingAway = 2, #Not using this (This state is useless)
    Cleaning = 3

class State:
    def __init__(self, name: BotStateNames, target: Point or Entity, bounds: Area) -> None:
        self.name = name
        self.target = target
        self.bounds = bounds

class StatefulBot(Bot):
    def __init__(self, namep: str, stateStack = []):
        super().__init__(namep)
        self.setStateStack(stateStack)

    def setStateStack(self, stateStack: list):
        if stateStack:
            self.state = stateStack.pop()
        self.stateToReturn = stateStack

    def move(self, canvas: Canvas, dt: float, registryActives: list, registryPassives: list):
        super().move(canvas, dt)
        self.updateState(registryActives, registryPassives)

    def approximateNumberOfMovesTo(self, object) -> int:
        theta = self.angleYaxis(object)
        turningLeft = (self.theta + 2.0 * math.pi - theta)  % (2.0 * math.pi)
        turningRight = (2.0 * math.pi - self.theta + theta) % (2.0 * math.pi)
        turningTillAlignment = min(turningLeft, turningRight)
        return self.distanceTo(object) / Bot.straightMovementVelocity + round(turningTillAlignment / 0.15)

    def reached(self, object: Point or Entity or Area or Dirt, registryPassives: list) -> bool:
        if isinstance(object, Point):
            return self.distanceTo(object) < Bot.hitBoxSize
        elif isinstance(object, Area):
            return self.isInArea(object)
        elif isinstance(object, Dirt):
            return object not in registryPassives
        else:
            return self.distanceTo(self.state.target) < Bot.hitBoxSize and self.isAligned(self.state.target)

    def updateMovingToTargetState(self, registryPassives):
        if self.reached(self.state.target, registryPassives):
            self.state = None

    def updateMovingAway(self, minDistance = 50):
        if isinstance(self.state.target, list):
            targets = self.state.target
        else:
            targets = [self.state.target]
        
        for target in targets:
            if self.distanceTo(target) <= minDistance + 50:
                return
        self.state = None

    def updateCleaningState(self, registryPassives: list):
        if not self.isInArea(self.state.bounds):
            self.stateToReturn.append(self.state)
            self.state = State(BotStateNames.MovingToTarget, self.state.bounds, self.mapBoundaries)
            return
        target = self.findClosestDirt(registryPassives)
        if target == None:
            self.state = None
        else:
            self.stateToReturn.append(self.state)
            self.state = State(BotStateNames.MovingToTarget, target, self.state.bounds)
        
    def findClosestDirt(self, registryPassives: list) -> Dirt:
        minMoves = inf
        closestDirt = None
        for rr in registryPassives:
            if isinstance(rr, Dirt) and self.state.bounds.contains(rr):
                moves = self.approximateNumberOfMovesTo(rr)
                if moves < minMoves:
                    minMoves = moves
                    closestDirt = rr
        return closestDirt

    def isAreaOccupied(self, registryActives, area: Area):
        for rr in registryActives:
            if isinstance(rr, Bot) and rr is not self:
                if area.contains(rr):
                    return True
        return False

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
                self.state = self.stateToReturn.pop()
                self.updateState(registryActives, registryPassives)

    def avoidRunningOutOfBounds(self):
        if not self.currentlyTurning:
            super().avoidRunningOutOfBounds()

    def transferFunction(self):
        if self.state == None:
            return
        if self.reachingOutOfBounds(self.state.bounds):
            self.avoidRunningOutOfBounds()
            return
        else:
            self.currentlyTurning = False
        if self.state.name == BotStateNames.MovingToTarget:
            self.chooseDirectionToTarget()
        elif self.state.name == BotStateNames.MovingAway: 
            self.chooseDirectionAway()
        else:
            self.clean()

    def clean(self):
        pass

    def chooseDirectionAway(self):
        if isinstance(self.state.target, list) and len(self.state.target) > 1:
            angle = self.getAverageAngle(self.state.target)
            if isOpposite(self.theta, angle):
                self.vl = Bot.straightMovementVelocity
                self.vr = Bot.straightMovementVelocity
            else:
                self.vl, self.vr = self.getTurnDirection(angle)
            return
        elif not isinstance(self.state.target, list):
            target = self.state.target
        else:
            target = self.state.target[0]
        self.chooseDirectionAwayFromTarget(target)

    def getAverageAngle(self, targets):
        if not targets:
            return None
        else:
            target = targets.pop()
            angle1 = self.angleYaxis(target)
            angle2 = self.getAverageAngle(targets)
            if angle2 == None:
                return angle1
            average = (angle1 + angle2) / 2
            if(abs(angle1 - angle2) > math.pi):
                average += math.pi
            average %= (math.pi * 2)
            return average

    def chooseDirectionAwayFromTarget(self, target):
        if self.isOpposite(target) or self.isPerpendicular(target): 
            self.vl = Bot.straightMovementVelocity
            self.vr = Bot.straightMovementVelocity
        else:
            self.vl, self.vr= self.getTurnDirection(self.angleYaxis(target))

    def chooseDirectionToTarget(self):
        if self.isAligned(self.state.target):
            self.vl = Bot.straightMovementVelocity 
            self.vr = Bot.straightMovementVelocity 
        else:
            self.vr, self.vl = self.getTurnDirection(self.angleYaxis(self.state.target))