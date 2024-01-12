import matplotlib.pyplot as plt

class Car:
    """
    The car class
    """
    def __init__(self, id, orientation, column, row, length):
        """
        Initializes a new class
        
        Parameters:
        - id: Name of the car
        - orientation: H (horizontal) or V (vertical)
        - column: current position of car (starts with 1)
        - row: current position of car (starts with 1)
        - lenght: length of car (2 or three)
        """
        self.id = id
        self.orientation = orientation
        self.column = column 
        self.row = row
        self.length = length 

        # Discuss with TA: move colour assignment to board class?
        self.colours = ['blue', 'orange', 'green', 'purple', 'brown', 'pink', 'olive', 'cyan','yellow','gold', 'violet', 'plum', 'slateblue', 'navy', 'orchid', 'plum']
        
        # checks if car.id is 'X', if true car.colour is set to 'red'
        if self.id == 'X':
            colour = 'red'
        
        # if car.id is not 'X', car.colour is set to a colour out of the self.colours list in order. Cars adjesent to eachother will have a 
        # smaller change of getting the same colour  
        else: 
            index = ord(self.id[-1]) % len(self.colours) 
            colour = self.colours[index]

        self.colour = colour
        
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

    
    def draw(self, canvas):
        """
        Creates a simple representation of a car on an existing canvas.

        Input:
        - Canvas object (plt subplot)
        """

        # checks the orientation of the car object       
        if self.orientation == 'H':

            # creates a rectangle in horizontal oriantion with the parameters of the object car 
            car = plt.Rectangle((self.column, self.row), self.length, 1, facecolor= self.colour, edgecolor='black', lw=5)
        else:

            # creates a rectangle in vertical oriantion with the parameters of the object car
            car = plt.Rectangle((self.column, self.row), 1, self.length, facecolor= self.colour, edgecolor='black', lw=5)
        
        # adds the made rectangles to the board
        canvas.add_patch(car)

        # shows the id of the car in the plot 
        plt.text(self.column+0.5, self.row+0.5, self.id, fontsize = 10)
