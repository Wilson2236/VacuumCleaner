from area import Area
import constants
import math
import random
from tkinter import Canvas
from counter import Counter
import numpy as np
from dirt import Dirt
from entity import Entity
from point import Point
from geometry import *
from squaredArea import SquaredArea

# This is the baseline bot, that provides all the necessary movement functionality
class Bot(Entity):
    mapBoundaries = SquaredArea(Point(constants.size / 2, constants.size / 2), constants.size, "map")
    hitBoxSize = 20
    straightMovementVelocity = 5.0
    turningVelocity = 2.2

    def __init__(self, namep: str):
        super().__init__(Point(random.randint(200, constants.size - 200), random.randint(200, constants.size - 200)), name=namep)
        self.theta = random.uniform(0.0,2.0*math.pi)
        self.ll = Bot.hitBoxSize * 2 #axle width
        self.vl = 0.0
        self.vr = 0.0
        self.currentActionMoves = 0
        self.currentlyTurning = False

    def isAligned(self, object) -> bool:
        return isAligned(self.theta, self.angleYaxis(object))

    def isOpposite(self, object) -> bool:
        return isOpposite(self.theta, self.angleYaxis(object))

    def isPerpendicular(self, object) -> bool:
        isPerpendicular(self.theta, self.angleYaxis(object))

    def isInArea(self, area: Area) -> bool:
        return area.contains(self.centralPoint)

    def getTurnDirection(self, angle):
        if (self.theta > angle and abs(self.theta - angle) <= math.pi) or (angle > self.theta and abs(self.theta - angle) > math.pi):
            return Bot.turningVelocity, -Bot.turningVelocity
        else:
            return -Bot.turningVelocity, Bot.turningVelocity

    def draw(self, canvas: Canvas):
        hitBoxOutline = [ 
            (self.centralPoint.x + Bot.hitBoxSize*math.sin(self.theta)) - Bot.hitBoxSize*math.sin((math.pi/2.0)-self.theta), 
            (self.centralPoint.y - Bot.hitBoxSize*math.cos(self.theta)) - Bot.hitBoxSize*math.cos((math.pi/2.0)-self.theta), 
            (self.centralPoint.x - Bot.hitBoxSize*math.sin(self.theta)) - Bot.hitBoxSize*math.sin((math.pi/2.0)-self.theta), 
            (self.centralPoint.y + Bot.hitBoxSize*math.cos(self.theta)) - Bot.hitBoxSize*math.cos((math.pi/2.0)-self.theta), 
            (self.centralPoint.x - Bot.hitBoxSize*math.sin(self.theta)) + Bot.hitBoxSize*math.sin((math.pi/2.0)-self.theta), 
            (self.centralPoint.y + Bot.hitBoxSize*math.cos(self.theta)) + Bot.hitBoxSize*math.cos((math.pi/2.0)-self.theta), 
            (self.centralPoint.x + Bot.hitBoxSize*math.sin(self.theta)) + Bot.hitBoxSize*math.sin((math.pi/2.0)-self.theta), 
            (self.centralPoint.y - Bot.hitBoxSize*math.cos(self.theta)) + Bot.hitBoxSize*math.cos((math.pi/2.0)-self.theta)  
        ]

        canvas.create_polygon(hitBoxOutline, fill="blue", tags=self.name)

        self.sensors = [
            Entity(
                Point((self.centralPoint.x + (Bot.hitBoxSize - 10)*math.sin(self.theta)) + Bot.hitBoxSize*math.sin((math.pi/2.0)-self.theta), 
                (self.centralPoint.y - (Bot.hitBoxSize - 10)*math.cos(self.theta)) + Bot.hitBoxSize*math.cos((math.pi/2.0)-self.theta))
            ),
            Entity(
                Point((self.centralPoint.x - (Bot.hitBoxSize - 10)*math.sin(self.theta)) + Bot.hitBoxSize*math.sin((math.pi/2.0)-self.theta), 
                (self.centralPoint.y + (Bot.hitBoxSize - 10)*math.cos(self.theta)) + Bot.hitBoxSize*math.cos((math.pi/2.0)-self.theta))
            )
        ]
    
        canvas.create_oval(
            self.centralPoint.x - round(Bot.hitBoxSize/2), self.centralPoint.y - round(Bot.hitBoxSize/2),
            self.centralPoint.x + round(Bot.hitBoxSize/2), self.centralPoint.y + round(Bot.hitBoxSize/2),
            fill="gold",
            tags=self.name
        )

        self.wheelAxes = [
            Entity(
                Point(self.centralPoint.x - Bot.hitBoxSize*math.sin(self.theta), 
                self.centralPoint.y + Bot.hitBoxSize*math.cos(self.theta))
            ),
            Entity(
                Point(self.centralPoint.x + Bot.hitBoxSize*math.sin(self.theta), 
                self.centralPoint.y - Bot.hitBoxSize*math.cos(self.theta))
            )
        ]

        # Draw wheels on the wheel axes
        canvas.create_oval(
            self.wheelAxes[0].centralPoint.x - 3, self.wheelAxes[0].centralPoint.y - 3,
            self.wheelAxes[0].centralPoint.x + 3, self.wheelAxes[0].centralPoint.y + 3,
            fill="red",
            tags=self.name
        )

        canvas.create_oval(
            self.wheelAxes[1].centralPoint.x - 3, self.wheelAxes[1].centralPoint.y - 3,
            self.wheelAxes[1].centralPoint.x + 3, self.wheelAxes[1].centralPoint.y + 3,
            fill="green",
            tags=self.name
        )

        canvas.create_oval(
            self.sensors[0].centralPoint.x - 3, self.sensors[0].centralPoint.y - 3, 
            self.sensors[0].centralPoint.x + 3, self.sensors[0].centralPoint.y + 3, 
            fill="yellow",
            tags=self.name
        )
        canvas.create_oval(
            self.sensors[1].centralPoint.x - 3, self.sensors[1].centralPoint.y - 3, 
            self.sensors[1].centralPoint.x + 3, self.sensors[1].centralPoint.y + 3, 
            fill="yellow",
            tags=self.name
        )
        
    # cf. Dudek and Jenkin, Computational Principles of Mobile Robotics
    def move(self, canvas: Canvas, dt: float):
        if self.vl==self.vr:
            R = 0
        else:
            R = (self.ll / 2.0) * ((self.vr + self.vl) / (self.vl - self.vr))
        
        omega = (self.vl - self.vr) / self.ll
        ICC = Point(self.centralPoint.x - R * math.sin(self.theta), self.centralPoint.y + R * math.cos(self.theta))
        m = np.matrix( 
            [ 
                [math.cos(omega * dt), -math.sin(omega * dt), 0], 
                [math.sin(omega * dt), math.cos(omega * dt), 0],  
                [0,0,1] 
            ] 
        )
        v1 = np.matrix(
            [
                [self.centralPoint.x-ICC.x],
                [self.centralPoint.y-ICC.y],
                [self.theta]
            ]
        )
        v2 = np.matrix(
            [
                [ICC.x],
                [ICC.y],
                [omega*dt]
            ]
        )
        newv = np.add(np.dot(m,v1),v2)
        newX = newv.item(0)
        newY = newv.item(1)
        newTheta = newv.item(2)
        newTheta = newTheta % (2.0 * math.pi) #make sure angle doesn't go outside [0.0,2*pi)
        self.centralPoint.x = newX
        self.centralPoint.y = newY
        self.theta = newTheta  

        if self.vl==self.vr: # straight line movement
            self.centralPoint.x += self.vr * math.cos(self.theta) #vr wlog
            self.centralPoint.y += self.vr * math.sin(self.theta)

        try:
            canvas.delete(self.name)
            self.draw(canvas)
        except:
            pass

    def getBoundaries(self, area: Area):
        xMin, xMax, yMin, yMax = area.getBoundaries()
        xMin += Bot.hitBoxSize * 0.75
        xMax -= Bot.hitBoxSize * 0.75
        yMin += Bot.hitBoxSize * 0.75
        yMax -= Bot.hitBoxSize * 0.75
        
        return xMin, xMax, yMin, yMax
        
    def reachingOutOfBounds(self, area: Area) -> bool:
        xMin, xMax, yMin, yMax = area.getBoundaries()

        return (self.centralPoint.x < xMin and math.cos(self.theta) < 0)  or \
            (self.centralPoint.x > xMax and math.cos(self.theta) > 0) or\
            (self.centralPoint.y < yMin and math.sin(self.theta) < 0) or\
            (self.centralPoint.y > yMax and math.sin(self.theta) > 0)

    def closestOutOfBoundsPoint(self, area: Area):
        xMin, xMax, yMin, yMax = area.getBoundaries()

        x, y = -1, -1
        if (self.centralPoint.x < xMin and math.cos(self.theta) < 0):
            x = xMin
        elif (self.centralPoint.x > xMax and math.cos(self.theta) > 0):
            x = xMax
        if (self.centralPoint.y < yMin and math.sin(self.theta) < 0):
            y = yMin
        elif (self.centralPoint.y > yMax and math.sin(self.theta) > 0):
            y = yMax
        if x == -1:
            x = self.centralPoint.x
        if y == -1:
            y = self.centralPoint.y

        return Point(x, y)

    def distanceFromSensorsTo(self, object):
        return self.distanceFromRightSensorTo(object), self.distanceFromLeftSensorTo(object)

    def distanceFromRightSensorTo(self, object) -> float:
        return self.sensors[0].distanceTo(object)

    def distanceFromLeftSensorTo(self, object) -> float:
        return self.sensors[1].distanceTo(object)

    def collectDirt(self, canvas: Canvas, registryPassives: list, count: Counter, map: np.ndarray) -> list:
        toDelete = []
        for idx,rr in enumerate(registryPassives):
            if isinstance(rr, Dirt):
                if self.distanceTo(rr) < Bot.hitBoxSize:
                    map[rr.centralPoint.x][rr.centralPoint.y] = 0
                    canvas.delete(rr.name)
                    toDelete.append(idx)
                    count.itemCollected()
        for ii in sorted(toDelete,reverse=True):
            del registryPassives[ii]
        return registryPassives, map

    def avoidRunningOutOfBounds(self):
        point = self.closestOutOfBoundsPoint(Bot.mapBoundaries)
        self.vl, self.vr = self.getTurnDirection(self.angleYaxis(point))
        self.currentlyTurning = True
        self.currentActionMoves = 0

    def transferFunction(self):
        if not self.currentlyTurning and self.reachingOutOfBounds(Bot.mapBoundaries):
            self.avoidRunningOutOfBounds()
            return
        self.wanderAround()

        if self.currentActionMoves == 0 and not self.currentlyTurning:
            self.currentActionMoves = random.randrange(10, 20)
            self.currentlyTurning = True
        if self.currentActionMoves == 0 and self.currentlyTurning:
            self.currentActionMoves = random.randrange(20, 50)
            self.currentlyTurning = False
        
        
    def wanderAround(self):
        # wandering behaviour
        self.vl = -Bot.turningVelocity
        self.vr = Bot.turningVelocity
        if self.currentlyTurning == False:
            self.vl = Bot.straightMovementVelocity
            self.vr = Bot.straightMovementVelocity
            
        self.currentActionMoves -= 1
        
        
        