from typing import Union
from pygame.math import Vector2

import mapping
from enemy import Enemy
from actionsdir import level_actions

def update_item_visibility(level, item):
    """
    Update an item's visibility: items should only be visible at their origin chunk
    """
    if(level.curr_chunk.id == item.origin):
        if(not item.visible):
            item.sprite.setPos(item.pos)
            item.visible = True
    else:
        if(item.visible):
            item.sprite.setPos((-100, -100))
            item.visible = False

def update_door(level, door, type):
    """
    Updates map state representation
    """
    update_item_visibility(level, door)
    if(door.sprite.rect.center[0] < 0 and door.represented == True):
        level_actions.clear_posarray(level, door.posarray)
        door.represented = False

    elif(door.sprite.rect.center[0] >= 0 and door.represented == False):
        level_actions.paint_posarray(level, door.posarray, (mapping.STAIR_UP if type else mapping.STAIR_DOWN))
        door.represented = True

#PICKAXE FUNCTIONS
def update_pickaxe_sprite(player, pickaxe):
    pickaxe.angle -= 7
    pic, pac = pickaxe.sprite.rect.center, player.sprite.rect.center
    offset = Vector2(30,30)
    pickaxe.sprite.rect.center = pac + offset.rotate(pickaxe.angle)

def update_pickaxe(level, pickaxe, player):
    if(player.inventory['P']):update_pickaxe_sprite(player, pickaxe)
    if(pickaxe.picked):return
    update_item_visibility(level, pickaxe)
    level_actions.paint_posarray(level, pickaxe.posarray, mapping.PICKAXE)

#ORB functions
def update_orb_sprite(player, orb):
    orb.angle -= 7
    pic, pac = orb.sprite.rect.center, player.sprite.rect.center
    offset = Vector2(50,50)
    orb.sprite.rect.center = pac + offset.rotate(orb.angle)

def update_orb(level, orb, player):
    if(player.inventory['O'] == True):update_orb_sprite(player, orb)
    if(orb.picked):return
    update_item_visibility(level, orb)
    level_actions.paint_posarray(level, orb.posarray, mapping.ORB)

def pick_pickUp(level, pickup, player):
    px, py = player.pos
    pickup.pick((px+2, py+2))
    level_actions.clear_posarray(level, pickup.posarray)
    player.inventory[str(pickup)] = False

def use_pickup(pickup, player):
    if(pickup.picked == False):return
    player.inventory[str(pickup)] = True - player.inventory[str(pickup)]
    if(not player.inventory[str(pickup)]):
        pickup.sprite.setPos((-100, -100))
        pickup.visible = False