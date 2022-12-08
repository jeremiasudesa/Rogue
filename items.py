from typing import Union
from sprite import Sprite

numeric = Union[float, int]

class Item:
    def __init__(self, type, pos, path, origin_chunk = 0):
        self.type = type
        self.sprite = Sprite(path, pos)
        self.sprite.setPos(pos)
        self.posarray = []
        self.origin = origin_chunk
        self.represented = False
        self.visible = False
        self.pos = pos
        self.gone = False
        self.name = "item"
    def getPosRect(self, width, height):
        ret = []
        for x in range(height):
            for y in range(width):
                ret.append((self.pos[0]+x, self.pos[1] + y))
        return ret

class Pickup(Item):
    def __init__(self, type, pos, path, origin_chunk = 0):
        super().__init__(type, pos, path, origin_chunk)

    def pick(self, playpos):
        self.sprite.rect.center = (playpos)
        self.picked, self.visible = True, False
        self.sprite.setPos((-100, -100))


class Door(Item):
    def __init__(self, level_a, level_b, pos):
        self.level_a, self.level_b = level_a, level_b
        if(self.level_a < self.level_b):
            sprite_path = 'portal1.png'
        else:
            sprite_path = 'portal2.png'
        super().__init__('DOOR', pos, sprite_path)
        self.sprite.setPos(pos)
        self.posarray = self.getPosRect(5,5)
        
    def __str__(self) -> str:
        return "D"
    
class Pickaxe(Pickup):
    def __init__(self, pos):
        super().__init__('pickaxe', pos, 'pick.png')
        self.posarray = self.getPosRect(2, 2)
        self.picked = False
        #TODO: turn every position to vector?
        self.angle = 0
    def __str__(self) -> str:
        return "P"

class Orb(Pickup):
    def __init__(self, pos):
        super().__init__('Orbimus Maximus', pos, 'orb.png')
        self.posarray = self.getPosRect(2, 2)
        self.picked = False
        self.angle = 0
    def __str__(self) -> str:
        return "O"
