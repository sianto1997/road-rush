import matplotlib.pyplot as plt

class Car:
    """
    The car class
    """
    def __init__(self, id, orientation, column, row, length):
        """
        Initializes a new class
        
        Parameters:
        - id (string): Name of the car
        - orientation (char): H (horizontal) or V (vertical)
        - column (int): current position of car (starts with 1)
        - row (int): current position of car (starts with 1)
        - length (int): length of car (2 or 3)
        """
        self.id = id
        self.orientation = orientation
        self.column = column 
        self.row = row
        self.length = length 

        # Discuss with TA: move colour assignment to board class?
        self.colours = ['blue', 'orange', 'green', 'purple', 'brown', 'pink', 'olive', 'cyan','yellow','gold', 'violet', 'plum', 'slateblue', 'navy', 'orchid', 'plum']
        
        # Checks if car.id is 'X', if true car.colour is set to 'red'
        if self.id == 'X':
            colour = 'red'
        
        # If car.id is not 'X', car.colour is set to a colour out of the self.colours list in order. Cars adjesent to eachother will have a 
        # Smaller change of getting the same colour  
        else: 
            index = ord(self.id[-1]) % len(self.colours) 
            colour = self.colours[index]

        self.colour = colour
        
    def update_collision_map(self, collision_map):
        """
        Update the collision map to include the current car. (add 1's)

        Input & output:
        - collision_map (np array of size [board_size + 2, board_size + 2])
        """
        location_column = self.column
        location_row = self.row

        # _ signifies that the variable itself will not be used
        for _ in range(self.length):
            collision_map[location_row][location_column] = self.id
            if self.orientation == 'H':
                location_column += 1
            else:
                location_row += 1
    
        return collision_map

    def get_pos(self):
        """
        
        """
        if self.orientation == 'H':
            return self.column
        
        return self.row