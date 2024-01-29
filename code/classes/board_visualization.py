import matplotlib.pyplot as plt


class BoardVisualization():

    def __init__(self, draw_interval):
        '''
        Initializes the board so that only one display is created

        Input:
        - draw_interval (float): The default value for the draw_interval. See draw function for more info.
        '''
        self.initialized = False
        self.draw_interval = draw_interval

    def init_visualization(self):
        '''
        Initializes the board so that only one display is created. Previously located in board, this created problems when visualizing multiple states (starting a lot of visualizations simultaneously).
        '''
        # Give the range to the figure
        self.canvas = plt.figure(figsize = [self.board.size + 0.5, self.board.size + 0.5])

        # Makes the background colour of the figure gray
        self.canvas.patch.set_facecolor('gray')

        # Creates the grid place
        self.ax = self.canvas.add_subplot()

        # Give the range to the figure
        self.canvas = plt.figure(figsize = [self.board.size + 0.5, self.board.size + 0.5])

        # Makes the background colour of the figure gray
        self.canvas.patch.set_facecolor('gray')

        # Creates the grid place
        self.ax = self.canvas.add_subplot()
        self.initialized = True
    
    def replace(self, board):
        '''
        Replace the existing board with a new one. Used for examining child states and new experiments.
        
        Input:
        - board (Board): The new board
        '''
        self.board = board

        # Initialize (only if not already initialized)
        if not self.initialized:
            self.init_visualization()

    def draw(self, draw_interval = 0):
        '''
        Draws the object board to the current state.
    
        Input:
        - draw_interval (float): A number between 0.0001 and 1000.0. This float is for showing a part of the simulation longer. By default, it uses the configured draw_interval.
        '''
        if not self.initialized:
            return
        
        if draw_interval == 0:
            draw_interval = self.draw_interval
        
        # Inverts the values of the y-axis
        self.ax.invert_yaxis()
        
        # Loops over the values of the x-axis
        for x in range(1, self.board.size + 1):
            # Makes a black line on the places of the x in a particular range 
            self.ax.plot([x, x], [1, self.board.size + 1], 'k')
        
        # Makes the exit row line
        self.ax.plot([self.board.size + 1, self.board.size + 1], [1, self.board.exit_row], 'k')
        self.ax.plot([self.board.size + 1, self.board.size + 1], [self.board.exit_row + 1,self.board.size + 1], 'k')

        # Loops over the values of y-axis
        for y in range(1, self.board.size + 2):

            # Makes a black line on the places of the y in a particular range
            self.ax.plot([1, self.board.size + 1], [y, y], 'k')
        
        # Create marges around the grid 
        self.ax.set_position([0, 0, 1, 1])

        # Deletes the axis numbers 
        self.ax.set_axis_off()

        for car in self.board.cars:
            self.draw_car(self.board.cars[car])
      
        plt.draw()
        # Pause to be able to show the visualization
        plt.pause(self.draw_interval)

        self.ax.cla()

    def close(self):
        '''
        Closes the visualization.
        '''
        plt.close(self.canvas)

    def draw_car(self, car):
        '''
        Creates a simple representation of a car on an existing canvas.

        Input:
        - car (Car): The car to draw.
        '''

        # Checks the orientation of the car object       
        if car.orientation == 'H':
            # Creates a rectangle in horizontal oriantion with the parameters of the object car 
            car_drawing = plt.Rectangle((car.column, car.row), car.length, 1, facecolor = car.colour, edgecolor = 'black', lw = 5)
        else:
            # Creates a rectangle in vertical oriantion with the parameters of the object car
            car_drawing = plt.Rectangle((car.column, car.row), 1, car.length, facecolor = car.colour, edgecolor = 'black', lw = 5)
        
        # Adds the made rectangles to the board
        self.ax.add_patch(car_drawing)

        # Shows the id of the car in the plot 
        plt.text(car.column + 0.5, car.row + 0.5, car.id, fontsize = 10)