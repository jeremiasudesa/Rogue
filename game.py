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


if __name__ == "__main__":
    pygame.init()
    #TODO:change player spawnpoint
    pos = [0, 0]
    player = Human("Lancelot", pos, PIXEL)
    player.updatePos()
    #create sprite group
    group = pygame.sprite.RenderPlain()
    group.add(player.sprite)
    map = mapping.Level(ROWS, COLUMNS)
    #visual interface
    interface = Interface(HEIGHT, WIDTH, PIXEL)
    interface.setSprites(group)
    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:            # check for key releases
                player.moving -=  1
            if event.type == pygame.KEYDOWN:          # check for key presses 
                player.moving += 1         
                if event.key == pygame.K_a:        # left arrow turns left
                    player.changeDir((-1, 0),0)
                elif event.key == pygame.K_d:     # right arrow turns right
                    player.changeDir((1, 0), 180)
                elif event.key == pygame.K_w:        # up arrow goes up
                    player.changeDir((0, -1), 270)
                elif event.key == pygame.K_s:     # down arrow goes down
                    player.changeDir((0, 1), 90)
        #TODO: move function that collapse player's movement to grid
        #TODO: remove the recreation of group
        player.updatePos()
        interface.setBackground(map.tilemap)
        interface.render()
    # Hacer algo con keys:
    # move player and/or gnomes

    # Salió del loop principal, termina el juego

