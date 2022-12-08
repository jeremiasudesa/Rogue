import pygame
import random

PIXEL = 10
ROWS = 90
COLUMNS = 120
HEIGHT = PIXEL*ROWS
WIDTH = COLUMNS*PIXEL
FRAME = 4000
SONGFREQ = 1000000
ANGLES = [270, 0, 180, 90]
DIRS = [(-1, 0), (0, -1), (0, 1), (1, 0)]
DIFFICULTY = 10
enemies = 0
enemychunk = 0
enemyseed = 0
chunks = 0
#dir and keys
keys = [pygame.K_w, pygame.K_a, pygame.K_d, pygame.K_s]
number_keys = [pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9]
dirdict = {}
for i in range(len(keys)):
    dirdict[keys[i]] = (DIRS[i], ANGLES[i])
ORIGIN_SEED = random.randint(0, 100000)