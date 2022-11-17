import pygame
import os

class Sprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super(Sprite, self).__init__()
        self.image = pygame.image.load(os.path.join('resources', name))
        self.rect = self.image.get_rect()
        self.rect.center = (0, 0)
        self.angle = 0
        self.iterations = 0

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle += angle

    def setPos(self, pos, step):
        self.rect.center = ((pos[1]+1) * step, (pos[0]+1) * step)
