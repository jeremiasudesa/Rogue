import pygame
from mapping import Tile

Location = tuple[int, int]

class Interface:
    """Interface
    Manage the visual representation of the game
    """
    def __init__(self, Height, Width, Pixel):
        self.Height, self.Width, self.Pixel = Height, Width, Pixel
        self.surf = pygame.display.set_mode((self.Width, self.Height))
        self.sprites = None

    def setBackground(self, map):
        """Background Image
        sets background image based on color map
        """
        self.bg = pygame.Surface((self.Width, self.Height))
        n, m = len(map), len(map[0])
        for i in range(n):
            for j in range(m):
                pygame.draw.rect(self.bg, map[i][j].color, pygame.Rect(j * self.Pixel, self.Pixel * i,self.Pixel, self.Pixel))
    
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