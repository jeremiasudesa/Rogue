import pygame
from mapping import Tile

Location = tuple[int, int]

class Interface:
    """Interface
    Manage the visual representation of the game
    """
    def __init__(self, Width, Height, Pixel):
        self.Width, self.Height, self.Pixel = Width, Height, Pixel
        self.surf = pygame.display.set_mode((self.Width, self.Height))
        self.sprites = None

    def setBackground(self, map):
        """Background Image
        sets background image based on color map
        """
        self.bg = pygame.Surface((self.Width, self.Height))
        for i in range(len(map)):
            for j in range(len(map[0])):
                pygame.draw.rect(self.bg, map[i][j].color, pygame.Rect(self.Pixel*i, self.Pixel*j, self.Pixel*(i+1), self.Pixel*(j+1)))
    
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
        pygame.display.flip()