from entity import Entity


class Human(Entity):
    def __init__(self, name, pos, moving = 0):
        super().__init__(name, pos,'pattto.png', 50)
        self.treasure, self.moving, self.dir = None, moving, (0, 0)
        self.XP = 0
        self.posarray = self.getPosRect(2, 2)
        self.inventory = {}
        self.inventory['P'], self.inventory['O'], self.inventory['T'] = None, None, None

