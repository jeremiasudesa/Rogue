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

PIXEL = 20
ROWS = 50
COLUMNS = 50
WIDTH = COLUMNS*PIXEL
HEIGHT = ROWS*PIXEL
TRESHOLD = 15000
iterations = 0

if __name__ == "__main__":
    interface = Interface(HEIGHT, WIDTH, PIXEL)
    pygame.init()
    level = mapping.Level(ROWS, COLUMNS)
    #TODO:change player spawnpoint
    pos = [8, 2]
    player = Human("Lancelot", pos, PIXEL, 1)
    actions.update_playpos(player, level, interface)
    actions.paint_player(player, level)
    #create sprite group
    group = pygame.sprite.RenderPlain()
    group.add(player.sprite)
    #visual interface
    interface.setSprites(group)
    #game loop pastor con maiz
    interface.setBackground(level.tilemap)
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
        if(iterations == TRESHOLD):
            iterations = 0
            actions.update_playpos(player, level, interface)
            interface.render()
        else:
            iterations += 1
    # Hacer algo con keys:
    # move player and/or gnomes

    # Salió del loop principal, termina el juego

