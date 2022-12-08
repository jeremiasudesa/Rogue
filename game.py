#!/usr/bin/env python3
import mapping
import sys

from human import Human
from actionsdir import actions, level_actions, interface_actions, player_actions, entities_actions, items_actions
import pygame
from interface import Interface
import music
import vars

iterations = 0

def initPygame():
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('Duck Rogue')

if __name__ == "__main__":
    #Pygame
    initPygame()
    #Store the game components
    gc = {}
    #Level
    level_actions.initLevel(gc)
    #Entities
    gc['elems'] = {}
    ge = gc['elems']
    entities_actions.initEntities(gc, ge)
    actions.spawn_enemy_batch(gc['level'], ge['player'], ge['enemies'])
    #Interface
    interface_actions.initInterface(gc)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and (event.key in (vars.keys)):            # check for key releases
                ge['player'].moving -=  1
            if event.type == pygame.KEYDOWN:          # check for key prXesses 
                if(event.key in (vars.keys)):
                    ge['player'].moving += 1 
                    ge['player'].dir = tuple(vars.DIRS[vars.keys.index(event.key)])
                    player_actions.handle_player_dir(ge['player'],event.key)
                elif(event.key == pygame.K_p):
                    items_actions.use_pickup(ge['pick'], ge['player'])
                elif(event.key == pygame.K_SPACE):
                    if(ge['player'].inventory['O']):actions.death_ray(gc['level'], gc['interface'], ge['player']) 
                elif(event.key == pygame.K_o):
                    items_actions.use_pickup(ge['orb'], ge['player'])
        if(iterations == vars.FRAME):
            #MUSIC
            music.rand_music("end.wav")
            iterations = 0
            #Loopify
            interface_actions.update_chunk_counter(gc['interface'], gc['elems']['player'])
            actions.update_enemies(gc)
            actions.update_player(gc)
            items_actions.update_door(gc['level'], ge['door1'], False)
            items_actions.update_door(gc['level'], ge['door2'], True)
            items_actions.update_pickaxe(gc['level'], ge['pick'], ge['player'])
            items_actions.update_orb(gc['level'], ge['orb'], ge['player'])
            gc['interface'].render()
        else:
            iterations += 1

