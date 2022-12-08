#!/usr/bin/env python3
import sys
from actionsdir import actions, level_actions, interface_actions, player_actions, entities_actions, items_actions, music_actions
import pygame
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
            match event.type:
                case pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                case pygame.KEYUP:
                    if(event.key in (vars.keys)): ge['player'].moving -=  1 
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_p:
                            items_actions.use_pickup(ge['pick'], ge['player'])
                        case pygame.K_o:
                            items_actions.use_pickup(ge['orb'], ge['player'])
                        case pygame.K_SPACE:
                            if(player_actions.in_inventory(ge['player'], 'O')):actions.death_ray(gc['level'], gc['interface'], ge['player']) 
                        case _:
                            if(event.key in (vars.keys)):player_actions.move(ge['player'], event.key)
        if(iterations == vars.FRAME):
            iterations = 0
            actions.frame(gc, ge)
        else:
            iterations += 1

