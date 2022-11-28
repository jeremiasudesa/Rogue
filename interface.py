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
    
    def fillScreen(self, color):
        pygame.draw.rect(self.bg, color, pygame.Rect(0, 0, const.WIDTH, const.HEIGHT))
        self.render()
    
    def createText(self, text, center, color = [255, 255, 255], bgcolor = [0, 0, 0]):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(text, True, color, bgcolor)
        textRect = text.get_rect()
        textRect.center = center
        self.surf.blit(text, textRect)
        pygame.display.update()
        return textRect
    
    def createQuestionText(self, text):
        self.createText(text, (const.WIDTH//2, const.HEIGHT//2))
    
    def writeUserInput(self, userstr):
        return self.createText(userstr, (const.WIDTH//2, const.HEIGHT//2 + 100))
    
    def clearText(self, rect):
        pygame.draw.rect(self.surf, [0, 0, 0], rect)
        pygame.display.update()

    def gameOver(self):
        self.fillScreen([255, 0, 0])
        self.createText("GAME OVER", (const.WIDTH//2, const.HEIGHT//2), bgcolor = [255, 0, 0])

