import pygame
import os
from sprite import Sprite

class Player:
    def __init__(self, name, xy, path, hit_points=50):
        self.name = name
        self.x, self.y = xy
        self.hp = hit_points
        self.max_hp = hit_points
        self.sprite = Sprite(xy, path)

    def loc(self):
        return self.x, self.y

    def move_to(self, xy):
        self.x, self.y = xy

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Player('{self.name}', '{self.loc}', '{self.hp}')"
