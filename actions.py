from typing import Union
from pygame.math import Vector2

import mapping
import pygame

#define player directions
angles = [270, 0, 180, 90]
dirs = []
it = 0
for i in range(-1, 2):
    for j in range(-1, 2):
        if(abs(i+j) == 1):
            dirs.append(((i, j), angles[it]))
            it+=1
keys = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s]
dirdict = {}
for i in range(len(keys)):
    dirdict[keys[i]] = dirs[i]

def handle_player_dir(player, key):
    player.changeDir([dirdict[key][0][0], dirdict[key][0][1]], dirdict[key][1])

def set_pvector(player, direction, angle):
    player.changeDir(direction, angle)

def paint_posarray(lvl, posarray, tile):
    for pos in posarray:
        lvl.state[pos[0]][pos[1]] = tile

def clear_posarray(lvl, posarray):
    for pos in posarray:
        lvl.state[pos[0]][pos[1]] = mapping.AIR

def nxt_chunk(gc, dir):
    '''
    Handle possible next chunk directions and pass it to the chunk object itself
    '''
    match dir[0]:
        case "U":
            gc['level'].upChunk(dir[1])
            gc['level'].update_map_chunk(gc['level'].curr_chunk.up)
        case "D":
            gc['level'].downChunk(dir[1])
            gc['level'].update_map_chunk(gc['level'].curr_chunk.down)
        case "L":
            gc['level'].leftChunk(dir[1])
            gc['level'].update_map_chunk(gc['level'].curr_chunk.left)
        case "R":
            gc['level'].rightChunk(dir[1])
            gc['level'].update_map_chunk(gc['level'].curr_chunk.right)
    gc['interface'].setBackground(gc['level'].tilemap)

def add_sprites(sprite_group, entity_list):
    for entity in entity_list.values():
        sprite_group.add(entity.sprite)

def nxt_level(gc, dir):
    if(gc['level'].adj_level[dir] == None):
        gc['level'].adj_level[dir] = mapping.Level(gc['level'].rows, gc['level'].columns, gc['level'].seed+1)
        gc['level'].adj_level[dir].adj_level['d' if (dir == 'u') else 'u'] = gc['level']
    gc['level'] = gc['level'].adj_level[dir]
    gc['interface'].setBackground(gc['level'].tilemap)
    pos = gc['level'].spawn
    gc['elems']['player'].posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1]]
    update_playpos(gc)
    paint_posarray(gc['level'], gc['elems']['door1'].posarray, mapping.STAIR_DOWN)
    paint_posarray(gc['level'], gc['elems']['door2'].posarray, mapping.STAIR_UP)

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
        print("clear_posarray")
        clear_posarray(level, door.posarray)
        door.represented = False

    elif(door.sprite.rect.center[0] >= 0 and door.represented == False):
        print("paint_posarray")
        paint_posarray(level, door.posarray, (mapping.STAIR_DOWN if type else mapping.STAIR_UP))
        door.represented = True

def update_pickaxe_sprite(player, pickaxe):
    pickaxe.angle -= 7
    pic, pac = pickaxe.sprite.rect.center, player.sprite.rect.center
    offset = Vector2(30,30)
    pickaxe.sprite.rect.center = pac + offset.rotate(pickaxe.angle)

def update_pickaxe(level, pickaxe, player):
    if(pickaxe.picked):
        update_pickaxe_sprite(player, pickaxe)
    update_item_visibility(level, pickaxe)
    paint_posarray(level, pickaxe.posarray, mapping.PICKAXE)

def pick_pickaxe(level, player, pickaxe):
    pickaxe.sprite.rect.center = (player.sprite.rect.center[0]+2, player.sprite.rect.center[0]+2)
    pickaxe.picked, pickaxe.visible = True, False
    clear_posarray(level, pickaxe.posarray)
    pickaxe.sprite.setPos((-100, -100))
    activate_destruction_mode(player)

def activate_destruction_mode(player):
    player.destructionMode = True

def destroy_walls(level, player, interface):
    nxt_pos = player.nxtPosarray(player.dir)
    for x in nxt_pos:
        if(x in player.posarray or level.whereIsPos(x)[0] != "I"):continue
        if(level.state[x[0]][x[1]] != mapping.WALL):continue
        level.state[x[0]][x[1]] = mapping.AIR
        level.tilemap[x[0]][x[1]].color = [0, 94, 184]
        interface.setBackground(level.tilemap)

def update_player(gc):
    update_playpos(gc)
    if(gc['elems']['player'].destructionMode):destroy_walls(gc['level'], gc['elems']['player'], gc['interface'])

def update_playpos(gc):
    """Update Player Position
    Updates the player's sprite position and the player representation in tilemap
    """
    #find next position
    nxtpos = gc['elems']['player'].nxtPosarray(gc['elems']['player'].dir)
    #check if player is trying to go outside the chunk
    dir = gc['level'].findBorder(nxtpos)
    if(dir[0] != "I"):
        nxt_chunk(gc, dir)
        chunkdir = [-dir[1][1], -dir[1][0]]
        nxtpos = gc['elems']['player'].nxtPosarray(dir[1])
        gc['elems']['player'].updatePos(nxtpos)
        paint_posarray(gc['level'], gc['elems']['player'].posarray, mapping.PLAYER)
        return
    #movement
    #TODO: make switch
    if(gc['elems']['player'].moving == False):return
    for pos in nxtpos:
        if(gc['level'].state[pos[0]][pos[1]] == mapping.STAIR_DOWN):
            nxt_level(gc, 'd')
            return
        elif(gc['level'].state[pos[0]][pos[1]] == mapping.STAIR_UP):
            nxt_level(gc, 'u')
            return
        elif(gc['level'].state[pos[0]][pos[1]] == mapping.PICKAXE):
            pick_pickaxe(gc['level'], gc['elems']['player'], gc['elems']['pick'])
        elif(gc['level'].is_walkable(pos) == False):return
    #TODO: hacer funcion clear_entity()
    clear_posarray(gc['level'], gc['elems']['player'].posarray)
    gc['elems']['player'].updatePos(nxtpos)
    paint_posarray(gc['level'], gc['elems']['player'].posarray, mapping.PLAYER)
