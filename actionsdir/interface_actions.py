from typing import Union
from pygame.math import Vector2

import pygame
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

def update_xp(interface, player):
    interface.drawCounter(player.XP)
