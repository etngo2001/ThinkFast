import json
class Unit:
    def __init__(self, name, cost, img_path, icon_path):
        self.name = name
        self.cost = cost
        self.img_path = img_path
        self.icon_path = icon_path
    
    def get_name(self):
        return self.name
    
    def get_cost(self):
        return self.cost
    
    def get_img_path(self):
        return self.img_path
    
    def get_icon_path(self):
        return self.icon_path