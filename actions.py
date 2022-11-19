from typing import Union


import mapping
import player
import pygame
import os

numeric = Union[int, float]

#TODO: UPDATE level-PLAYER REPRESENTATION

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
    player.changeDir([dirdict[key][0][0]*player.speed, dirdict[key][0][1]], dirdict[key][1])

def set_pvector(player, direction, angle):
    player.changeDir(direction, angle)

def paint_player(player, level):
    for pos in player.posarray:
        level.state[pos[0]][pos[1]] = mapping.PLAYER

def nxt_chunk(level, dir, interface):
    '''
    Handle possible next chunk directions and pass it to the chunk object itself
    '''
    match dir[0]:
        case "U":
            level.upChunk(dir[1])
            level.update_map_chunk(level.curr_chunk.up)
        case "D":
            level.downChunk(dir[1])
            level.update_map_chunk(level.curr_chunk.down)
        case "L":
            level.leftChunk(dir[1])
            level.update_map_chunk(level.curr_chunk.left)
        case "R":
            level.rightChunk(dir[1])
            level.update_map_chunk(level.curr_chunk.right)
    interface.setBackground(level.tilemap)


def update_playpos(player, level, interface):
    """Update Player Position
    Updates the player's sprite position and the player representation in tilemap
    """
    #find next position
    nxtpos = player.nxtPosarray(player.dir)
    #check if player is trying to go outside the chunk
    dir = level.findBorder(nxtpos)
    if(dir[0] != "I"):
        nxt_chunk(level, dir, interface)
        chunkdir = [-dir[1][1], -dir[1][0]]
        print(nxtpos)
        print(dir[1])
        nxtpos = player.nxtPosarray(dir[1])
        print(nxtpos)
        player.updatePos(nxtpos)
        paint_player(player, level)
        return
    #movement
    if(player.moving == False):return
    for pos in nxtpos:
        if(level.is_walkable(pos) == False):return
    #TODO: hacer funcion clear_entity()
    for pos in player.posarray:
        level.state[pos[0]][pos[1]] = mapping.AIR
    player.updatePos(nxtpos)
    paint_player(player, level)

# def clip(value: numeric, minimum: numeric, maximum: numeric) -> numeric:
#     if value < minimum:
#         return minimum
#     if value > maximum:
#         return maximum
#     return value


# #def attack(dungeon, player, ...): # completar
#     # completar
# #    raise NotImplementedError


# # def move_to(dungeon: mapping.Dungeon, player: player.Player, location: tuple[numeric, numeric]):
# #     # completar
# #     raise NotImplementedError


# # def move_up(dungeon: mapping.Dungeon, player: player.Player):
# #     # completar
# #     raise NotImplementedError


# def move_down(dungeon: mapping.Dungeon, player: player.Player):
#     # completar
#     raise NotImplementedError


# def move_left(dungeon: mapping.Dungeon, player: player.Player):
#     # completar
#     raise NotImplementedError


# def move_right(dungeon: mapping.Dungeon, player: player.Player):
#     # completar
#     raise NotImplementedError


# def climb_stair(dungeon: mapping.Dungeon, player: player.Player):
#     # completar
#     raise NotImplementedError


# def descend_stair(dungeon: mapping.Dungeon, player: player.Player):
#     # completar
#     raise NotImplementedError


# def pickup(dungeon: mapping.Dungeon, player: player.Player):
#     # completar
#     raise NotImplementedError
