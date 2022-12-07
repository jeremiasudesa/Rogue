from typing import Union
from pygame.math import Vector2

import mapping
import pygame
import const
import random
from enemy import Enemy
import sys
import time
import music
import items
import bisect

def initLevelItems(ge, level):
    ge['door1'], ge['door2'] = items.Door(1, 2, level.downStair), items.Door(1, 0, level.upStair)
    if(level.pickaxe != None): ge['pick'] = items.Pickaxe(level.pickaxe)
    if(level.orb != None): ge['orb'] = items.Orb(level.orb)

#TODO: distinction between regular keys and number_keys
keys = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s]
number_keys = [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]
dirdict = {}
for i in range(len(keys)):
    dirdict[keys[i]] = (const.DIRS[i], const.ANGLES[i])
