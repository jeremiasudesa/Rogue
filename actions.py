from typing import Union


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
    gc['entities']['player'].posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1]]
    update_playpos(gc)

#esto es HORRIBLE, pero se puede ignorar
def update_door(gc, door, type):
    if(gc['level'].curr_chunk.id == 0):
        if(not door.visible):
            door.sprite.setPos(door.pos)
            door.visible = True
        paint_posarray(gc['level'], door.posarray, (mapping.STAIR_DOWN if type else mapping.STAIR_UP))
    else:
        if(door.visible):
            door.sprite.setPos((-100, -100))
            door.visible = False
        clear_posarray(gc['level'], door.posarray)

def update_playpos(gc):
    """Update Player Position
    Updates the player's sprite position and the player representation in tilemap
    """
    #find next position
    nxtpos = gc['entities']['player'].nxtPosarray(gc['entities']['player'].dir)
    #check if player is trying to go outside the chunk
    dir = gc['level'].findBorder(nxtpos)
    if(dir[0] != "I"):
        nxt_chunk(gc, dir)
        chunkdir = [-dir[1][1], -dir[1][0]]
        nxtpos = gc['entities']['player'].nxtPosarray(dir[1])
        gc['entities']['player'].updatePos(nxtpos)
        paint_posarray(gc['level'], gc['entities']['player'].posarray, mapping.PLAYER)
        return
    #movement
    if(gc['entities']['player'].moving == False):return
    for pos in nxtpos:
        if(gc['level'].state[pos[0]][pos[1]] == mapping.STAIR_DOWN):
            nxt_level(gc, 'd')
            return
        elif(gc['level'].state[pos[0]][pos[1]] == mapping.STAIR_UP):
            nxt_level(gc, 'u')
            return
        elif(gc['level'].is_walkable(pos) == False):return
    #TODO: hacer funcion clear_entity()
    clear_posarray(gc['level'], gc['entities']['player'].posarray)
    gc['entities']['player'].updatePos(nxtpos)
    paint_posarray(gc['level'], gc['entities']['player'].posarray, mapping.PLAYER)