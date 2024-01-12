
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
        print(self.id, colour, 'Column:', self.column, 'Row:',self.row)
        
    def update_collision_map(self, collision_map):
        location_column = self.column
        location_row = self.row

        # _ signifies that the variable itself will not be used
        for _ in range(self.length):
            collision_map[location_row][location_column] = 1
            if self.orientation == 'H':
                location_column += 1
            else:
                location_row += 1
    
        return collision_map
        
    def try_move(self, collision_map, steps):
        
        if self.orientation == 'H':
            collision_map_slice = collision_map[self.row]
            start_pos = self.column
        else:
            collision_map_slice = collision_map[:,self.column]
            start_pos = self.row

        offset = 0
        if steps > 0:
            offset = self.length
        else:
            offset = steps

        # print(self.column, self.row)
        # print(offset, start_pos, steps, start_pos + steps, abs(steps))
        start_pos = max(0, start_pos + offset)
        end_pos = min(start_pos+abs(steps), len(collision_map_slice))
        # print(start_pos, end_pos, abs(steps))
        target_area = collision_map_slice[start_pos:end_pos] == 1
        
        print(target_area)
        if not target_area.any() and len(target_area) > 0:
            if self.orientation == 'H':
                self.column += steps
            else:
                self.row += steps
            
            print(f'Move of car {self.id} ({self.orientation}) successful: {steps}')
            return True

        print(f'Move of car {self.id} ({self.orientation}) was unsuccessful: {steps}')
        return False
    
    def draw(self, board):
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

        # shows the id of the car in the plot 
        plt.text(self.column+0.5, self.row+0.5, self.id, fontsize = 10)
