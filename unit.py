class Unit:
    def __init__(self, name, cost, level, origin, group):
        self.name = name
        self.cost = cost
        self.level = level
        self.origin = origin
        self.group = group

    def __str__(self):
        return f"{self.name} {self.cost} {self.level} {self.origin} {self.group}"
    
    def levelUp(self, level):
        self.level += 1