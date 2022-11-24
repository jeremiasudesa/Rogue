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

def initEntities(ge):
    ge['player'] = Human("Lancelot", gc['level'].spawn)
    ge['door1'], ge['door2'] = Door(1, 2, gc['level'].downStair), Door(1, 0, gc['level'].upStair)
    ge['pick'] = Pickaxe(gc['level'].pickaxe)
    ge['enemies'] = []

def initInteface(gc):
    #Interface
    gc['interface'] = Interface()
    #create sprite group
    gc['sprite_group'] = pygame.sprite.RenderPlain()
    actions.add_sprites(gc['sprite_group'], (gc['elems']))
    #visual interface
    gc['interface'].setSprites(gc['sprite_group'])
    gc['interface'].setBackground(gc['level'].tilemap)

def initLevel(gc):
    gc['level'] = mapping.Level(const.ROWS, const.COLUMNS, 1)

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
    initInteface(gc)
    while True:
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
                    actions.handle_player_dir(ge['player'],event.key)
                if(event.key == pygame.K_p):
                    actions.use_pickaxe(ge['player'], ge['pick'])
        if(iterations == const.FRAME):
            #TODO: turn this into a music.py functionality
            #MUSIC
            num = random.randint(0, const.SONGFREQ)
            if(num == 0 and music.music_channel.get_busy() == False):
                music.play_song("end.mp3")
            iterations = 0
            #Loopify
            actions.update_player(gc)
            actions.update_door(gc['level'], ge['door1'], False)
            actions.update_door(gc['level'], ge['door2'], True)
            actions.update_pickaxe(gc['level'], ge['pick'], ge['player'])
            gc['interface'].render()
        else:
            iterations += 1

