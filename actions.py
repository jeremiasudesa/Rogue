from typing import Union


import mapping
import player
import pygame
import os

numeric = Union[int, float]

#TODO: UPDATE MAP-PLAYER REPRESENTATION

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
    print(f"hola {direction}")
    player.changeDir(direction, angle)

def paint_player(player, map):
    for pos in player.posarray:
        map.state[pos[0]][pos[1]] = mapping.PLAYER

def update_playpos(player, map):
    """Update Player Position
    Updates the player's sprite position and the player representation in tilemap
    """
    if(player.moving == False):return
    nxtposarray = []
    for pos in player.posarray:
        trypos = (player.dir[0] + pos[0], player.dir[1] + pos[1])
        if(map.is_walkable(trypos) == False):return
        nxtposarray.append(trypos)
    for pos in player.posarray:
        map.state[pos[0]][pos[1]] = mapping.AIR
    player.updatePos(nxtposarray)
    paint_player(player, map)

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
