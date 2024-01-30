import matplotlib.pyplot as plt


class BoardVisualization():
    '''
    This class manages the visualization of the experiments

    Attributes
    ----------
    initialized : Boolean
        Starts at False to make the figure, then is set to True so only one figures exists
    draw_interval : float
        The default value for the draw_interval. See draw function for more info
    '''

    def __init__(self, draw_interval):
        self.initialized = False
        self.draw_interval = draw_interval

    def init_visualization(self):
        '''
        Initializes the board so that only one display is created
        '''
        self.canvas = plt.figure(figsize = [self.board.size + 0.5, self.board.size + 0.5])
        self.canvas.patch.set_facecolor('gray')
        self.ax = self.canvas.add_subplot()
        self.initialized = True
    
    def replace(self, board):
        '''
        Replace the existing board with a new one. Used for examining child states and new experiments
        
        Parameter
        ---------
        - board : Board
            The new board
        '''
        self.board = board

        if not self.initialized:
            self.init_visualization()

    def draw(self, draw_interval = 0):
        '''
        Draws the object board to the current state
    
        Parameter
        - draw_interval : float
            A number between 0.0001 and 1000.0. shows a part of the simulation longer (default is 0)
        '''
        if not self.initialized:
            return
        
        if draw_interval == 0:
            draw_interval = self.draw_interval
        
        self.ax.invert_yaxis()
        
        for x in range(1, self.board.size + 1):
            self.ax.plot([x, x], [1, self.board.size + 1], 'k')
        
        self.ax.plot([self.board.size + 1, self.board.size + 1], [1, self.board.exit_row], 'k')
        self.ax.plot([self.board.size + 1, self.board.size + 1], [self.board.exit_row + 1,self.board.size + 1], 'k')

        for y in range(1, self.board.size + 2):
            self.ax.plot([1, self.board.size + 1], [y, y], 'k')
        
        self.ax.set_position([0, 0, 1, 1])
 
        self.ax.set_axis_off()

        for car in self.board.cars:
            self.draw_car(self.board.cars[car])
      
        plt.draw()
        plt.pause(self.draw_interval)

        self.ax.cla()

    def close(self):
        '''
        Closes the visualization
        '''
        plt.close(self.canvas)

    def draw_car(self, car):
        '''
        Creates a simple representation of a car on an existing canvas

        Parameter
        ---------
        car : Car
            The car to draw
        '''      
        if car.orientation == 'H': 
            car_drawing = plt.Rectangle((car.column, car.row), car.length, 1, facecolor = car.colour, edgecolor = 'black', lw = 5)
        else:
            car_drawing = plt.Rectangle((car.column, car.row), 1, car.length, facecolor = car.colour, edgecolor = 'black', lw = 5)
        
        self.ax.add_patch(car_drawing)

        plt.text(car.column + 0.5, car.row + 0.5, car.id, fontsize = 10)