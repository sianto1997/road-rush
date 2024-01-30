class Car:
    '''
    The car class that is used for placing cars on a board

    Attributes
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
    colour : str
        The color of this car (used in visualization), red if the car id = 'X'
    '''
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
        
        if self.id == 'X':
            colour = 'red'
        else: 
            index = ord(self.id[-1]) % len(self.colours) 
            colour = self.colours[index]

        self.colour = colour
        
    def update_collision_map(self, collision_map):
        '''
        Update the collision map to include the current car (add the cars id on the right positions)

        Parameters
        ----------
        collision_map : numpy.chararray 
            The existing collision_map that needs to be updated

        Output
        ------
        collision_map : numpy.chararray
            The updated collision_map with this car placed on it
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

        Parameters
        ----------
        opposite : bool
            Get the other coordinate (horizontal car -> row or vertical car -> column) (default = False)
        '''
        if self.orientation == 'H' and not opposite or self.orientation == 'V' and opposite:
            return self.column
        
        return self.row