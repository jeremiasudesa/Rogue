import random
from player import Player
import pygame


class Human(Player):
    def __init__(self, name, xy, PIXEL):
        self.x, self.y = xy[0]*PIXEL, xy[1]*PIXEL
        super().__init__(name, (self.x, self.y),'pato.png', 50)
        self.weapon = None
        self.treasure = None
        self.tool = None
        self.alive = True

    def updatePos(self):
        self.sprite.update()

    def damage(self):
        if self.sword:
            return random.random() * 20 + 5
        return random.random() * 10 + 1

    def kill(self):
        self.hp = 0
        self.alive = False

    #def has_sword(self):
        # completar
