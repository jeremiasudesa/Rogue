from typing import Union
from pygame.math import Vector2

import mapping
import pygame
import vars
import random
from enemy import Enemy
import sys
import time
import music
import items
import bisect

def handle_player_dir(player, key):
    player.changeDir([vars.dirdict[key][0][0], vars.dirdict[key][0][1]], vars.dirdict[key][1])

def set_pvector(player, direction, angle):
    player.changeDir(direction, angle)