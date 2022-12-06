from entity import Entity

#TODO: probablemente eliminar la clase player y remplazarla por human

class Human(Entity):
    def __init__(self, name, pos, moving = 0):
        super().__init__(name, pos,'pattto.png', 50)
        self.weapon, self.treasure, self.tool, self.alive, self.moving, self.dir = None, None, None, True, moving, (0, 0)
        #Change for inventory dictionary
        self.destructionMode, self.deathPower = False, False
        self.sprite.setPos(self.pos)
        self.chunkCounter = 0
        self.posarray = self.getPosRect(2, 2)

