#!/usr/bin/env python3
import mapping
import sys

import random
from human import Human
from items import Door
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
    ge['player'] = Human("Lancelot", gc['level'].spawn, const.PIXEL, 1)
    ge['door1'], ge['door2'] = Door(1, 2, gc['level'].downStair, const.PIXEL), Door(1, 0, gc['level'].upStair, const.PIXEL)

def initInteface(gc):
    #Interface
    gc['interface'] = Interface()
    #create sprite group
    gc['sprite_group'] = pygame.sprite.RenderPlain()
    actions.add_sprites(gc['sprite_group'], (gc['entities']))
    #visual interface
    gc['interface'].setSprites(gc['sprite_group'])
    gc['interface'].setBackground(gc['level'].tilemap)

def initLevel(gc):
    gc['level'] = mapping.Level(const.ROWS, const.COLUMNS, 0)

if __name__ == "__main__":
    #Pygame
    initPygame()
    #Store the game components
    gc = {}
    #Level
    initLevel(gc)
    #Entities
    gc['entities'] = {}
    ge = gc['entities']
    initEntities(ge)
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
            if event.type == pygame.KEYDOWN:          # check for key presses 
                if(event.key in (actions.keys)):
                    ge['player'].moving += 1 
                    actions.handle_player_dir(ge['player'],event.key)
        if(iterations == const.FRAME):
            #TODO: turn this into a music.py functionality
            #MUSIC
            num = random.randint(0, const.SONGFREQ)
            if(num == 0 and music.music_channel.get_busy() == False):
                music.play_song("end.mp3")
            iterations = 0
            actions.update_playpos(gc)
            actions.update_door(gc, ge['door1'])
            actions.update_door(gc, ge['door2'])
            gc['interface'].render()
        else:
            iterations += 1

