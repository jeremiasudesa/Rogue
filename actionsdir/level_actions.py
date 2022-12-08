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

def initLevel(gc):
    gc['level'] = mapping.Level(vars.ROWS, vars.COLUMNS, 1000)

def initLevelItems(ge, level):
    ge['door1'], ge['door2'] = items.Door(1, 2, level.downStair), items.Door(1, 0, level.upStair)
    if(level.pickaxe != None): ge['pick'] = items.Pickaxe(level.pickaxe)
    if(level.orb != None): ge['orb'] = items.Orb(level.orb)

def nxt_chunk(gc, level, dir):
    '''
    Handle possible next chunk directions and pass it to the chunk object itself
    '''
    if(level.curr_chunk.adj_chunks[dir[0]] == None):gc['elems']['player'].XP += 1
    level.newChunk(dir[1], dir[0])
    level.update_map_chunk(level.curr_chunk.adj_chunks[dir[0]])

def get_ray(level, pos, component_id, ray, play_dir, depth):
    if(depth == 700 or level.where[pos[0]][pos[1]] != component_id):return
    ray.append(pos)
    probdir = 0.45
    probodir = (1 - probdir)/3
    prob = [probdir if play_dir == vars.DIRS[i] else probodir for i in range(len(vars.DIRS))]
    curr_dir = random.choices(vars.DIRS, prob)[0]
    new_pos = (pos[0] + curr_dir[0], pos[1] + curr_dir[1])
    if(level.is_walkable(new_pos)):get_ray(level, new_pos, component_id, ray, play_dir, depth+1)

def paint_posarray(lvl, posarray, tile):
    for pos in posarray:
        lvl.state[int(pos[0])][int(pos[1])] = tile

def clear_posarray(lvl, posarray):
    for pos in posarray:
        lvl.state[int(pos[0])][int(pos[1])] = mapping.AIR