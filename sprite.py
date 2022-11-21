import pygame
import os
#from interface import PIXEL

class Sprite(pygame.sprite.Sprite):
    def __init__(self, path, pos):
        super(Sprite, self).__init__()
        self.image = pygame.image.load(os.path.join('resources', path))
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.angle = 0
        self.iterations = 0

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle += angle

    def setPos(self, pos):
        self.rect.center = ((pos[1]+1) * 10, (pos[0]+1) * 10)
