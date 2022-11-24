from entity import Entity

class Enemy(Entity):
    def __init__(self, name, pos, moving = 0):
        super().__init__(name, pos,'enemy.png', 50)
        self.weapon, self.treasure, self.alive, self.moving, self.dir = None, None, True, moving, [0, 0]
        self.sprite.setPos(self.pos)
        self.posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1]]