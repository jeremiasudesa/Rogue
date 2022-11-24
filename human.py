from entity import Entity

#TODO: probablemente eliminar la clase player y remplazarla por human

class Human(Entity):
    def __init__(self, name, pos, moving = 0):
        super().__init__(name, pos,'niupat.png', 50)
        self.weapon, self.treasure, self.tool, self.alive, self.moving, self.dir = None, None, None, True, moving, [0, 0]
        self.destructionMode = False
        self.sprite.setPos(self.pos)
        self.posarray = [pos,[pos[0], pos[1]+1], [pos[0]+1, pos[1]], [pos[0]+1, pos[1]+1]]

