#!/usr/bin/env python3
import mapping
import sys

from human import Human
from actionsdir import actions, level_actions, interface_actions, player_actions, entities_actions, items_actions, music_actions
import pygame
from interface import Interface
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
                            player_actions.move(ge['player'], event.key)
        if(iterations == vars.FRAME):
            #MUSIC
            music_actions.rand_music("end.wav")
            iterations = 0
            #Loopify
            interface_actions.update_xp(gc['interface'], gc['elems']['player'])
            actions.update_enemies(gc)
            actions.update_player(gc)
            items_actions.update_door(gc['level'], ge['door1'], False)
            items_actions.update_door(gc['level'], ge['door2'], True)
            items_actions.update_pickaxe(gc['level'], ge['pick'], ge['player'])
            items_actions.update_orb(gc['level'], ge['orb'], ge['player'])
            interface_actions.render_interface(gc['interface'])
        else:
            iterations += 1

