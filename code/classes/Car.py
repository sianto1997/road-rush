
import matplotlib.pyplot as plt

class Car:
    def __init__(self, id, orientation, column, row, length):
        self.id = id
        self.orientation = orientation
        self.column = column 
        self.row = row
        self.length = length 
        self.colours = ['blue', 'orange', 'green', 'purple', 'brown', 'pink', 'olive', 'cyan']
        if self.id == 'X':
            colour = 'red'
        else: 
            index = ord(self.id[-1]) % len(self.colours) 
            colour = self.colours[index]
        
        
        self.colour = 'tab:' + colour
        print(colour)
        
    def visualize_car(self, board):
        
        if self.id == 'X':
            print(self.column, self.row)
        
        if self.orientation == 'H':
            car = plt.Rectangle((self.column, self.row), self.length, 1, facecolor= self.colour, edgecolor='black', lw=5)
        else:
            car = plt.Rectangle((self.column, self.row), 1, self.length, facecolor= self.colour, edgecolor='black', lw=5)
        board.add_patch(car) 
        board.text(0.5, 0.5, self.id, color='white', ha='center', va='center', fontsize=10, zorder=2)
        
        
        
    
