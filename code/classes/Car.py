import random
import matplotlib.pyplot as plt

class Car:
    def __init__(self, id, orientation, column, row, length):
        self.id = id
        self.orientation = orientation
        self.column = column 
        self.row = row
        self.length = length 
        self.colours = ['blue', 'orange', 'green', 'purple', 'brown', 'pink', 'geel',]
        if self.id == 'X':
            colour = 'red'
        else: 
            colour = self.colours[random.randint(0,6)]
        
        self.colour = 'tab:' + colour
        print(colour)
        
    def visualize_car(self, board):
        if self.id == 'X':
            print(self.column, self.row)
        #fig, ax = plt.subplots(figsize=(self.length, 1) if self.orientation == 'horizontal' else (1, self.length))
        rect = plt.Rectangle((self.column, self.row), self.length, 1, facecolor= self.colour, edgecolor='black')
        board.add_patch(rect) 
        
    
