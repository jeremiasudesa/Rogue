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
COLUMNS = 90
WIDTH = COLUMNS*PIXEL
HEIGHT = ROWS*PIXEL
TRESHOLD = 20000
iterations = 0

if __name__ == "__main__":
    pygame.init()
    map = mapping.Level(ROWS, COLUMNS)
    #TODO:change player spawnpoint
    pos = [8, 2]
    player = Human("Lancelot", pos, PIXEL, 1)
    actions.update_playpos(player, map)
    actions.paint_player(player, map)
    #create sprite group
    group = pygame.sprite.RenderPlain()
    group.add(player.sprite)
    #visual interface
    interface = Interface(HEIGHT, WIDTH, PIXEL)
    interface.setSprites(group)
    #game loop pastor con maiz
    interface.setBackground(map.tilemap)
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
            actions.update_playpos(player, map)
            interface.render()
        else:
            iterations += 1
    # Hacer algo con keys:
    # move player and/or gnomes

    # Salió del loop principal, termina el juego

