from typing import Union
from sprite import Sprite

numeric = Union[float, int]

class Item:
    def __init__(self, type, pos, path):
        self.type = type
        self.sprite = Sprite(path, pos)
        self.sprite.setPos(pos)

class Door(Item):
    def __init__(self, level_a, level_b, pos, step):
        self.level_a, self.level_b, self.pos, self.step = level_a, level_b, pos, step
        if(self.level_a < self.level_b):
            sprite_path = 'door1.png'
        else:
            sprite_path = 'door2.png'
        super().__init__('DOOR', pos, sprite_path)
        self.sprite.setPos(pos)
        self.visible = True
    

# class Sword(Item):
#     def __init__(self, name: str, fc: str, min_dmg: numeric, max_dmg: numeric):
#         super().__init__(name, fc, 'weapon')
#         self.min_dmg = min_dmg
#         self.max_dmg = max_dmg


# class Amulet(Item):
#     def __init__(self, name: str, fc: str):
#         super().__init__(name, fc, 'treasure')


# class PickAxe(Item):
#     def __init__(self, name: str, fc: str):
#         super().__init__(name, fc, 'tool')
