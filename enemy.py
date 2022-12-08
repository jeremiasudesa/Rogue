from entity import Entity
from pygame.math import Vector2
from random import randint

class Enemy(Entity):
    def __init__(self, name, pos, ORIGIN_SEED, moving = True):
        super().__init__(name, pos,'enemy.png', 64)
        self.alive, self.moving = True, moving
        self.sprite.setPos(self.pos)
        self.dir = Vector2(1 - 2*randint(0, 1), 1 - 2*randint(0, 1))
        self.posarray = self.getPosRect(2, 2)
        self.origin = ORIGIN_SEED