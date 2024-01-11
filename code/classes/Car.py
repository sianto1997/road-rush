
import matplotlib.pyplot as plt

class Car:
    def __init__(self, id, orientation, column, row, length):
        self.id = id
        self.orientation = orientation
        self.column = column 
        self.row = row
        self.length = length 
        self.colours = ['blue', 'orange', 'green', 'purple', 'brown', 'pink', 'olive', 'cyan','yellow','gold', 'violet', 'plum', 'slateblue', 'navy', 'orchid', 'plum']
        if self.id == 'X':
            colour = 'red'
        else: 
            index = ord(self.id[-1]) % len(self.colours) 
            colour = self.colours[index]

        self.colour = colour
        print(colour)
        
    def update_grid(self, grid):
        location_column = self.column
        location_row = self.row

        # _ signifies that the variable itself will not be used
        for _ in range(self.length):
            grid[location_row - 1][location_column - 1] = 1
            if self.orientation == 'H':
                location_column += 1
            else:
                location_row += 1
    
        return grid
    # def get_end_pos(self):
    #     if self.orientation == 'H':
    #         return self.column + self.length
        
    #     return self.row + self.length

        
    def try_move(self, grid, steps):
        

        if self.orientation == 'H':
            grid_slice = grid[:, self.row]
            start_pos = self.column
        else:
            grid_slice = grid[self.column, :]
            start_pos = self.row

        end_pos = start_pos + steps
        
        # Disable the car's own area to 0 (otherwise it will say it cannot move because the own car is there)
        grid_slice[start_pos:self.length] = 0

        
        
        if steps < 0:
            start_pos -= steps
        print(grid_slice)
        print(abs(steps), steps, start_pos)
        target_area = grid_slice[start_pos:abs(steps)] == 1

        print(target_area)
        if target_area & True:
            return True
            # if self.orientation == 'H':
            #     self.column += step

        return False

    def move(self, steps):
        if self.orientation == 'H':
            self.column += steps
        else:
            self.row += steps

        print(f'Move of car {self.id} ({self.orientation}) successful: {steps}')

    
    def visualize_car(self, board):
        """
        creates a simple representation of a car 
        """

        # checks the orientation of the car object       
        if self.orientation == 'H':

            # creates a rectangle in horizontal oriantion with the parameters of the object car 
            car = plt.Rectangle((self.column, self.row), self.length, 1, facecolor= self.colour, edgecolor='black', lw=5)
        else:

            # creates a rectangle in vertical oriantion with the parameters of the object car
            car = plt.Rectangle((self.column, self.row), 1, self.length, facecolor= self.colour, edgecolor='black', lw=5)
        
        # adds the made rectangles to the board
        board.add_patch(car) 
        plt.text(self.column+0.5, self.row+0.5, self.id, fontsize = 10)
