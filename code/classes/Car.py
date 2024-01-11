import random

class Car:
    def __init__(self, id, orientation, column, row, length):
        self.id = id
        self.orientation = orientation
        self.column = column 
        self.row = row
        self.length = length 
        self.colours = ['blue', 'orange', 'green', 'purple', 'brown', 'pink', 'gray']
        if self.id == 'X':
            colour = 'red'
        else: 
            colour = self.colours[random.randint(0,6)]
        
        self.colour = 'tab:' + colour
        print(colour)
        
    def visualize(self):
        pass
    
