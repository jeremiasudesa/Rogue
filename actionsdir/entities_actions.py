from typing import Union
from pygame.math import Vector2

import mapping
import pygame
import vars
import random
from enemy import Enemy
import sys
import time
import items
import bisect
from human import Human
from actionsdir import level_actions

def initEntities(gc, ge):
    ge['player'] = Human("Lancelot", gc['level'].spawn)
    level_actions.initLevelItems(ge, gc['level'])
    ge['enemies'] = []

def add_sprites(sprite_group, entity):
    if(type(entity) == list):
        for x in entity:
            sprite_group.add(x.sprite)
    else:
        sprite_group.add(entity.sprite)

def add_sprites_from_dict(sprite_group, entity_list):
    for entity in entity_list.values():
        add_sprites(sprite_group, entity)

