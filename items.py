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

class Door(Item):
    def __init__(self, level_a, level_b, pos):
        self.level_a, self.level_b = level_a, level_b
        if(self.level_a < self.level_b):
            sprite_path = 'door1.png'
        else:
            sprite_path = 'door2.png'
        super().__init__('DOOR', pos, sprite_path)
        self.sprite.setPos(pos)
        #TODO: posarray maker taking into consideration width and height (also, I think that the player pos is discongruent with sprite center pos)
        self.posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1],[pos[0]+2, pos[1]], [pos[0]+2, pos[1]+1], [pos[0]+3, pos[1]], [pos[0]+3, pos[1]+1]]
    
#TODO: change name hammer?
class Pickaxe(Item):
    def __init__(self, pos):
        super().__init__('pickaxe', pos, 'pickaxe.png')
        self.posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1],[pos[0]+2, pos[1]]]
        self.picked = False
        #TODO: turn every position to vector?
        self.angle = 0

class Orb(Item):
    def __init__(self, pos):
        super().__init__('Orbimus Maximus', pos, 'ORB.png')
        self.posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1],[pos[0]+2, pos[1]]]
        self.picked = False
        self.angle = 0


# class Amulet(Item):
#     def __init__(self, name: str, fc: str):
#         super().__init__(name, fc, 'treasure')
