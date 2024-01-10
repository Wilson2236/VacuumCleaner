from tkinter import Canvas
from entity import Entity
from point import Point

class Dirt(Entity):

    def __init__(self, namep: str, point: Point):
        super().__init__(point, namep)

    def draw(self, canvas: Canvas):
        canvas.create_oval(
            self.centralPoint.x-1,self.centralPoint.y-1, 
            self.centralPoint.x+1,self.centralPoint.y+1, 
            fill="grey",
            tags=self.name
        )