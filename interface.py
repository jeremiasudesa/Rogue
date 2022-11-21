import pygame
from mapping import Tile
import const

Location = tuple[int, int]

class Interface:
    """Interface
    Manage the visual representation of the game
    """
    def __init__(self):
        self.surf = pygame.display.set_mode((const.WIDTH, const.HEIGHT))
        self.sprites = None

    def setBackground(self, map):
        """Background Image
        sets background image based on color map
        """
        self.bg = pygame.Surface((const.WIDTH, const.HEIGHT))
        n, m = len(map), len(map[0])
        for i in range(n):
            for j in range(m):
                pygame.draw.rect(self.bg, map[i][j].color, pygame.Rect(j * const.PIXEL, const.PIXEL * i,const.PIXEL, const.PIXEL))
    
    def setSprites(self, sprite_group):
        """Set Sprites
        sets current sprite group
        """
        self.sprites = sprite_group

    def render(self):
        """Render
        Blits background, then draws sprites
        """
        self.surf.blit(self.bg, (0,0))
        if(not self.sprites == None):self.sprites.draw(self.surf)
        pygame.display.update()