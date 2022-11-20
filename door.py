from sprite import Sprite

class Door():
    def __init__(self, level_a, level_b, pos, step):
        self.level_a, self.level_b, self.pos, self.step = level_a, level_b, pos, step
        if(self.level_a < self.level_b):
            self.sprite = Sprite('door1.png')
        else:
            self.sprite = Sprite('door2.png')
        self.sprite.setPos(pos,step)
        self.visible = True
    