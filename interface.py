import pygame
from mapping import Tile
import vars
import random

Location = tuple[int, int]

class Interface:
    """Interface
    Manage the visual representation of the game
    """
    def __init__(self):
        self.surf = pygame.display.set_mode((vars.WIDTH, vars.HEIGHT))
        self.sprites = None

    def setBackground(self, map):
        """Background Image
        sets background image based on color map
        """
        self.bg = pygame.Surface((vars.WIDTH, vars.HEIGHT))
        n, m = len(map), len(map[0])
        for i in range(n):
            for j in range(m):
                color = map[i][j].color
                f = 1
                color = (color[0]*f, color[1]*f, color[2]*f)
                pygame.draw.rect(self.bg, color, pygame.Rect(j * vars.PIXEL, vars.PIXEL * i,vars.PIXEL, vars.PIXEL))
    
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
        pygame.draw.rect(self.bg, color, pygame.Rect(0, 0, vars.WIDTH, vars.HEIGHT))
        self.render()
    
    def createText(self, text, center,surface, color = [255, 255, 255], bgcolor = [0, 0, 0]):
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(text, True, color, bgcolor)
        textRect = text.get_rect()
        textRect.center = center
        surface.blit(text, textRect)
        pygame.display.update()
        return textRect
    
    def createQuestionText(self, text):
        self.createText(text, (vars.WIDTH//2, vars.HEIGHT//2), self.surf)
    
    def writeUserInput(self, userstr):
        return self.createText(userstr, (vars.WIDTH//2, vars.HEIGHT//2 + 100), self.surf)
    
    def clearText(self, rect):
        pygame.draw.rect(self.surf, [0, 0, 0], rect)
        pygame.display.update()

    def gameOver(self):
        self.fillScreen([255, 0, 0])
        self.createText("GAME OVER", (vars.WIDTH//2, vars.HEIGHT//2), self.surf,  bgcolor = [255, 0, 0])

    def showRay(self, ray):
        for cell in ray:
            wob = random.randint(0, 1)
            pygame.draw.rect(self.bg, wob*[0, 255, 255] + (1-wob)*[255, 255, 255], pygame.Rect(cell[1] * vars.PIXEL, vars.PIXEL * cell[0],vars.PIXEL, vars.PIXEL))
        self.render()

    def clearRay(self, ray, tilemap):
        for cell in ray:
            pygame.draw.rect(self.bg, tilemap[cell[0]][cell[1]].color, pygame.Rect(cell[1] * vars.PIXEL, vars.PIXEL * cell[0],vars.PIXEL, vars.PIXEL))
        self.render()
    
    def drawCounter(self, chunk):
        self.createText(f"XP: {chunk}", (50,50), surface = self.bg, bgcolor=None)
