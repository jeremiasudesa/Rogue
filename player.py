import pygame
import os
from sprite import Sprite

class Player:
    def __init__(self, name, pos, path, hit_points=50):
        self.name = name
        self.pos = pos
        self.hp = hit_points
        self.max_hp = hit_points
        self.sprite = Sprite(path)

    def loc(self):
        return self.pos

    def move_to(self, pos):
        self.pos = pos

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Player('{self.name}', '{self.loc}', '{self.hp}')"
