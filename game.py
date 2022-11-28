#!/usr/bin/env python3
import mapping
import sys

import random
from human import Human
from items import Door, Pickaxe
import actions
import pygame
from interface import Interface
import music
import const

iterations = 0

def initPygame():
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.display.set_caption('Duck Rogue')

def initEntities(ge):
    ge['player'] = Human("Lancelot", gc['level'].spawn)
    actions.initLevelItems(ge, gc['level'])
    ge['enemies'] = []

def initInterface(gc):
    #Interface
    gc['interface'] = Interface()
    #create sprite group
    gc['sprite_group'] = pygame.sprite.RenderPlain()
    actions.add_sprites_from_dict(gc['sprite_group'], (gc['elems']))
    #visual interface
    gc['interface'].setSprites(gc['sprite_group'])
    gc['interface'].setBackground(gc['level'].tilemap)

def initLevel(gc):
    gc['level'] = mapping.Level(const.ROWS, const.COLUMNS, 100)

if __name__ == "__main__":
    #Pygame
    initPygame()
    #Store the game components
    gc = {}
    #Level
    initLevel(gc)
    #Entities
    gc['elems'] = {}
    ge = gc['elems']
    initEntities(ge)
    actions.spawn_enemy_batch(gc['level'], ge['player'], ge['enemies'])
    #Interface
    initInterface(gc)
    while True:
        #TODO: EVENT SWITCH
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and (event.key in (actions.keys)):            # check for key releases
                ge['player'].moving -=  1
            if event.type == pygame.KEYDOWN:          # check for key prXesses 
                if(event.key in (actions.keys)):
                    ge['player'].moving += 1 
                    ge['player'].dir = tuple(const.DIRS[actions.keys.index(event.key)])
                    actions.handle_player_dir(ge['player'],event.key)
                elif(event.key == pygame.K_p):
                    actions.use_pickaxe(ge['player'], ge['pick'])
                elif(event.key == pygame.K_SPACE):
                    if(ge['player'].deathPower):actions.death_ray(gc['level'], gc['interface'], ge['player']) 
                elif(event.key == pygame.K_o):
                    actions.use_orb(gc['level'], ge['player'], ge['orb'])
        if(iterations == const.FRAME):
            #TODO: turn this into a music.py functionality
            #MUSIC
            num = random.randint(0, const.SONGFREQ)
            if(num == 0 and music.music_channel.get_busy() == False):
                music.play_song("end.mp3")
            iterations = 0
            #Loopify
            actions.update_enemies(gc)
            actions.update_player(gc)
            actions.update_door(gc['level'], ge['door1'], False)
            actions.update_door(gc['level'], ge['door2'], True)
            actions.update_pickaxe(gc['level'], ge['pick'], ge['player'])
            actions.update_orb(gc['level'], ge['orb'], ge['player'])
            gc['interface'].render()
        else:
            iterations += 1

