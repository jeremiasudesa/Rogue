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
WIDTH = ROWS*PIXEL
HEIGHT = ROWS*PIXEL


if __name__ == "__main__":
    pygame.init()
    # initial parameters
    level = 0
    player = Human("Lancelot", [1, 1], PIXEL)
    group = pygame.sprite.RenderPlain()
    group.add(player.sprite)
    map = mapping.Level(ROWS, COLUMNS)
    interface = Interface(WIDTH, HEIGHT, PIXEL)
    turns = 0
    group = pygame.sprite.RenderPlain()
    group.add(player.sprite)
    interface.setSprites(group)
    #game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:            # check for key releases
                player.sprite.moving -=  1
            if event.type == pygame.KEYDOWN:          # check for key presses 
                print("A")
                player.sprite.moving += 1         
                if event.key == pygame.K_LEFT:        # left arrow turns left
                    player.sprite.changeDir((-PIXEL, 0),0)
                elif event.key == pygame.K_RIGHT:     # right arrow turns right
                    player.sprite.changeDir((PIXEL, 0), 180)
                elif event.key == pygame.K_UP:        # up arrow goes up
                    player.sprite.changeDir((0, -PIXEL), 270)
                elif event.key == pygame.K_DOWN:     # down arrow goes down
                    player.sprite.changeDir((0, PIXEL), 90)
        #TODO: move function that collaplayer.spritees movement to grid
        #TODO: remove the recreation of group
        player.updatePos()
        interface.setBackground(map.tilemap)
        interface.render()
    # Hacer algo con keys:
    # move player and/or gnomes

    # Salió del loop principal, termina el juego
