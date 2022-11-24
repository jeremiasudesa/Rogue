from sprite import Sprite

class Entity:
    def __init__(self, name, pos, path, hit_points=50):
        self.name = name
        self.pos = pos
        self.hp = hit_points
        self.max_hp = hit_points
        self.sprite = Sprite(path, pos)
        self.sprite.setPos(pos)

    def __plusDir(self, pos:tuple, dir):
        return [pos[0] + dir[0], pos[1] + dir[1]]

    def nxtPosarray(self, dir):
        '''
        Returns the next position if player moves along direction
        '''
        ret = []
        for pos in self.posarray:
            trypos = self.__plusDir(pos, dir)
            ret.append(trypos)
        return ret

    def updatePos(self, posarray):
        #move based on direction
        self.posarray = posarray
        self.sprite.setPos(self.posarray[0])

    def changeDir(self, dir, desired_angle):
        self.dir = dir
        self.sprite.rotate(desired_angle - self.sprite.angle)

    def loc(self):
        return self.pos

    def move_to(self, pos):
        self.pos = pos

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Entity('{self.name}', '{self.loc}', '{self.hp}')"

    
