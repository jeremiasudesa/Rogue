import random
from player import Player
import pygame

#TODO: probablemente eliminar la clase player y remplazarla por human

class Human(Player):
    def __init__(self, name, pos, step, speed, moving = False):
        super().__init__(name, pos,'niupat.png', 50)
        self.weapon = None
        self.treasure = None
        self.tool = None
        self.alive = True
        self.moving = moving
        self.dir = [0, 0]
        self.step = step
        self.sprite.setPos(self.pos, self.step)
        self.speed = speed
        self.posarray = [pos,[pos[0], pos[1]+speed], [pos[0]+speed, pos[1]], [pos[0]+speed, pos[1]+speed]]

    def updatePos(self, posarray):
        #move based on direction
        self.posarray = posarray
        self.sprite.setPos(self.posarray[0], self.step)

    def changeDir(self, dir, desired_angle):
        self.dir = dir
        self.sprite.rotate(desired_angle - self.sprite.angle)

