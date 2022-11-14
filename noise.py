# Importing the library
import pygame
import opensimplex
import sys
import math
import bisect

def linear_gradient(x, a, b, c, d, e):
    return 10*int(math.exp(a * (x+b)**2)*c + math.exp(d * (x+e)))

def R(x):
    return linear_gradient(x, -0.01, -18, 240, 0.07, -13)

def G(x):
    return linear_gradient(x, -0.012, -19, 225, 0.04, 45)

def B(x):
    return linear_gradient(x, -0.013, -19, 190, 0.07, -14)

def color(x):
    return (R(x), G(x), B(x))

def main():
    #TODO: clase celda
    #init noise grid
    opensimplex.seed(1234)
    n, m, s, k= 50,50,0.1, 1
    mat = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            for x in range(k):
                factor, scale = (1/2)**x, (x+1)*s
                mat[i][j] += factor * opensimplex.noise2(x = scale*i, y = scale*j)
            mat[i][j] += 1
            mat[i][j] /= 2
    #Pygame
    pygame.init()
    W ,H = 800, 800
    pixel = math.sqrt((W*H)//(n*m))
    surface = pygame.display.set_mode((W, H))
    #types
    __colors = [[0, 0, 51],[0, 94, 184], [160, 160, 160],[96, 96, 96],[32, 32, 32]]
    __heights = [-1, 0.35, 0.5, 0.7, 0.82]
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        for i in range(n):
            for j in range(m):
                #TODO: change to ranges
                color=__colors[bisect.bisect_left(__heights, mat[i][j])-1]
                pygame.draw.rect(surface, color, pygame.Rect(pixel*i, pixel*j, pixel*(i+1), pixel*(j+1)))
        pygame.display.flip()
        

if __name__ == "__main__":
    main() 