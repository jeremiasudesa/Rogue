import random
from player import Player
import pygame

#TODO: probablemente eliminar la clase player y remplazarla por human

class Human(Player):
    def __init__(self, name, pos, step, treshold = 2,moving = False):
        super().__init__(name, pos,'patonobordes.png', 50)
        self.weapon = None
        self.treasure = None
        self.tool = None
        self.alive = True
        self.treshold = treshold
        self.moving = moving
        self.iterations = 0
        self.dir = [-1, 0]
        self.step = step

    def updatePos(self):
        #slow the movements down
        self.iterations += 1
        if(self.iterations < self.treshold):return
        self.iterations = 0
        #move based on direction
        if(self.moving == 0):return
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]
        self.sprite.setPos(self.pos, self.step)

    def changeDir(self, dir, desired_angle):
        self.dir = dir
        self.sprite.rotate(desired_angle - self.sprite.angle)

    def damage(self):
        if self.sword:
            return random.random() * 20 + 5
        return random.random() * 10 + 1


    def kill(self):
        self.hp = 0
        self.alive = False

    #def has_sword(self):
        # completar
