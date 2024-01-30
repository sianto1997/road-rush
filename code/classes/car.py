class Car:
    def __init__(self, id, orientation, column, row, length):
        '''
        Initializes a new car class
        
        Parameters
        ----------
        id : str
            Name of the car
        orientation : char
            H (horizontal) or V (vertical)
        column : int
            Current position of car (starts with 1)
        row : int
            Current position of car (starts with 1)
        length : int
            Length of car (2 or 3)
        '''

        self.id = id
        self.orientation = orientation
        self.column = column 
        self.row = row
        self.length = length 

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
        '''
        Update the collision map to include the current car. (add 1's)

        Parameter
        ---------
        collision_map : numpy.chararray 
            size of the c
        '''

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

    def get_pos(self, opposite = False):
        '''
        Get the position of the car based on the orientation of the car. For a horizontal car this is the column, for the vertical car this is row.

        Input:
        - opposite : bool
            Get the other coordinate (horizontal car -> row or vertical car -> column) (default = False)
        '''
        if self.orientation == 'H' and not opposite or self.orientation == 'V' and opposite:
            return self.column
        
        return self.row