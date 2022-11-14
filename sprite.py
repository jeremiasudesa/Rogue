import pygame
import os

class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, name,treshold = 1,moving = False):
        super(Sprite, self).__init__()
        self.image = pygame.image.load(os.path.join('resources', name))
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = list(pos)
        self.dir = [-1, 0]
        self.moving = 0
        self.angle = 0
        self.treshold = treshold
        self.iterations = 0

    def rotate(self, angle):
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.angle += angle

    def update(self):
        self.iterations += 1
        if(self.iterations < self.treshold):return
        self.iterations = 0
        if(self.moving == 0):return
        print(self.pos)
        self.pos[0] += self.dir[0]
        self.pos[1] += self.dir[1]
        print(self.pos)
        self.rect.center = self.pos
    
    def changeDir(self, dir, desired_angle):
        self.dir = dir
        self.rotate(desired_angle - self.angle)