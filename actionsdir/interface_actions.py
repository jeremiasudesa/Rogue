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
from interface import Interface
from actionsdir import entities_actions

def initInterface(gc):
    #Interface
    gc['interface'] = Interface()
    #create sprite group
    gc['sprite_group'] = pygame.sprite.RenderPlain()
    entities_actions.add_sprites_from_dict(gc['sprite_group'], (gc['elems']))
    #visual interface
    gc['interface'].setSprites(gc['sprite_group'])
    gc['interface'].setBackground(gc['level'].tilemap)

def updateBakground(interface, level):
    interface.setBackground(level.tilemap)

def update_chunk_counter(interface, player):
    interface.drawCounter(player.XP)
