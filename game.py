#!/usr/bin/env python3
import time
import mapping
import magic
import sys

import random
from human import Human
from items import Item
import actions
import pygame
from interface import Interface
import music
from door import Door

PIXEL = 10
ROWS = 90
COLUMNS = 120
WIDTH = COLUMNS*PIXEL
HEIGHT = ROWS*PIXEL
FRAME = 10000
iterations = 0
song_freq = 1000

if __name__ == "__main__":
    interface = Interface(HEIGHT, WIDTH, PIXEL)
    pygame.init()
    level = mapping.Level(ROWS, COLUMNS)
    #TODO:change player spawnpoint
    pos = level.spawn
    player = Human("Lancelot", pos, PIXEL, 1)
    door1, door2 = Door(1, 2, level.downStair, PIXEL), Door(1, 0, level.upStair, PIXEL)
    actions.update_playpos(player, level, interface)
    actions.paint_player(player, level)
    #create sprite group
    group = pygame.sprite.RenderPlain()
    group.add(player.sprite)
    group.add(door1.sprite)
    group.add(door2.sprite)
    #visual interface
    interface.setSprites(group)
    #game loop pastor con maiz
    interface.setBackground(level.tilemap)
    pygame.mouse.set_visible(False)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP and (event.key in (actions.keys)):            # check for key releases
                player.moving -=  1
            if event.type == pygame.KEYDOWN:          # check for key presses 
                if(event.key in (actions.keys)):
                    player.moving += 1 
                    actions.handle_player_dir(player,event.key)
        if(iterations == FRAME):
            #TODO: turn this into a music.py functionality
            #MUSIC
            num = random.randint(0, song_freq)
            if(num == 0 and music.music_channel.get_busy() == False):
                music.play_song("end.mp3")
            iterations = 0
            actions.update_playpos(player, level, interface)
            interface.render()
        else:
            iterations += 1
    # Hacer algo con keys:
    # move player and/or gnomes

    # Salió del loop principal, termina el juego

