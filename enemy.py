from entity import Entity
from pygame.math import Vector2
from random import randint

class Enemy(Entity):
    def __init__(self, name, pos, origin_chunk, moving = 0):
        super().__init__(name, pos,'enemy.png', 50)
        self.weapon, self.treasure, self.alive, self.moving, self.dir = None, None, True, moving, [0, 0]
        self.sprite.setPos(self.pos)
        self.dir = Vector2(1 - 2*randint(0, 1), 1 - 2*randint(0, 1))
        self.moving = True
        self.posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1]]
        self.origin = origin_chunk