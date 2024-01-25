import matplotlib.pyplot as plt


class BoardVisualization():

    def __init__(self):
        """
        Initializes the board so that only one display is created
        """
        # self.replace(board)
        # give the range to the figure
        self.canvas = plt.figure(figsize=[self.board.size + 0.5, self.board.size + 0.5])

        # makes the background colour of the figure gray
        self.canvas.patch.set_facecolor('gray')

        # creates the grid place
        self.ax = self.canvas.add_subplot()
        self.initialized = False

    def init_visualization(self):
        """
        Initializes the board so that only one display is created
        """
        if not self.initialized:
            # give the range to the figure
            self.canvas = plt.figure(figsize=[self.board.size + 0.5, self.board.size + 0.5])

            # makes the background colour of the figure gray
            self.canvas.patch.set_facecolor('gray')

            # creates the grid place
            self.ax = self.canvas.add_subplot()
            self.initialized = True
    
    def replace(self, board):
        self.board = board
        self.init_visualization()

    def draw(self, ms=0.0001):
        """
        Draws the object board to the current state
        """
        # if not self.visualize:
        #     return
        
        # inverts the values of the y-axis
        self.ax.invert_yaxis()
        # loops over the values of the x-axis
        for x in range(1,self.board.size+1):
            
            # makes a black line on the places of the x in a particular range 
            self.ax.plot([x, x], [1, self.board.size + 1], 'k')
        
        # makes the exit row line
        self.ax.plot([self.board.size+1, self.board.size+1], [1,self.board.exit_row], 'k')
        self.ax.plot([self.board.size+1, self.board.size+1], [self.board.exit_row+1,self.board.size+1], 'k')

        # loops over the values of y-axis
        for y in range(1, self.board.size + 2):

            # makes a black line on the places of the y in a particular range
            self.ax.plot([1, self.board.size + 1], [y,y], 'k')
        
        # create marges around the grid 
        self.ax.set_position([0, 0, 1, 1])

        # deletes the axis numbers 
        self.ax.set_axis_off()
        # print(self.cars)
        for car in self.board.cars:
            self.board.cars[car].draw(self.ax)
      
        plt.draw()
        # Pause to be able to show the visualization
        plt.pause(ms)
        # plt.savefig('foto-for-esmee')

        self.ax.cla()

    def pause(self, ms):

        self.draw(ms)
        # plt.draw()

        # plt.pause(ms)
        # self.ax.cla()

    def close(self):
        plt.close(self.canvas)