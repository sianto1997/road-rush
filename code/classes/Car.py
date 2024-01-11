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

    def update_grid(self, grid):
        location_column = self.column
        location_row = self.row

        # _ signifies that the variable itself will not be used
        for _ in range(1, self.length):
            grid[location_column - 1][location_row - 1] = 1
            if self.orientation == 'H':
                location_column += 1
            else:
                location_row += 1
    
        return grid
    
