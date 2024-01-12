import matplotlib.pyplot as plt
import pandas as pd
from car import Car 
from math import ceil
import numpy as np

class Board:   
    def __init__(self, input_file, visualize=False):
        """
        Creates a board for the game Rush Hour
        - input_file = CSV, the file with information about the board 
        """ 
        self.visualize = visualize
        # get position of 'hour' in title of input file
        start = input_file.find('hour') + len('hour')
        
        # get position of 'x' in title of input file, starting from position 'hour'
        end = input_file.find('x', start)
        
        # extract substring between 'hour' and 'x', convert to  integer and remove whitespaces
        self.size = int(input_file[start:end].strip())
        self.exit_row = ceil(self.size / 2)
        self.cars = []
        print(self.size, self.exit_row)

        # TODO for Esmée
        # self.moves = 
        if (visualize):
            self.init_visualization()

    def record_move(self, car_id, step):
        self.moves = []
        self.moves.append((car_id,step))
        print(self.moves)

    def save_moves(self, output_filename):
        pass

    def add_cars(self, csv):

        # loops over the index and rows of the given dataframe 
        for index, row in csv.iterrows():

            # creates the car obejct with the information of the dataframe
            car = Car(row.car, row.orientation, row.col, row.row, row.length)
    
            # appends the object car to the list self.cars 
            self.cars.append(car)

            # Saving m
            if car.id == 'X':
                self.red_car = car


        # print(self.map_grid())
    
    def init_visualization(self):
        """
        Initializes the board so that only one display is created
        """
        # give the range to the figure
        board = plt.figure(figsize=[self.size + 0.5, self.size + 0.5])

        # makes the background colour of the figure gray
        board.patch.set_facecolor('gray')

        # creates the grid place
        self.ax = board.add_subplot()


    def draw(self):
        """
        Draws the object board to the current state
        """
        if not self.visualize:
            return
        
        # inverts the values of the y-axis
        self.ax.invert_yaxis()
        # loops over the values of the x-axis
        for x in range(1,self.size+1):
            
            # makes a black line on the places of the x in a particular range 
            self.ax.plot([x, x], [1, self.size + 1], 'k')
        
        # makes the exit row line
        self.ax.plot([self.size+1, self.size+1], [1,self.exit_row], 'k')
        self.ax.plot([self.size+1, self.size+1], [self.exit_row+1,self.size+1], 'k')

        # loops over the values of y-axis
        for y in range(1, self.size + 2):

            # makes a black line on the places of the y in a particular range
            self.ax.plot([1, self.size + 1], [y,y], 'k')
        
        # create marges around the grid 
        self.ax.set_position([0, 0, 1, 1])

        # deletes the axis numbers 
        self.ax.set_axis_off()

        for car in self.cars:
            car.draw(self.ax)
      
        plt.draw()
        plt.pause(0.7)

        self.ax.cla()

    def try_move(self, car, steps):
        grid = self.get_collision_map()
     
        if car.try_move(grid, steps):
            self.draw()
            self.record_move(car.id, steps)

    def get_collision_map(self):
        row_bound = np.ones((1, self.size))
        column_bound = np.ones((self.size + 2, 1))

        collision_map = np.zeros((self.size, self.size))

        collision_map = np.vstack((row_bound, collision_map, row_bound))
        collision_map = np.hstack((column_bound, collision_map, column_bound))

        # Unblock exit row
        collision_map[self.exit_row][self.size+1] = 0
        
        for car in self.cars:
            collision_map = car.update_collision_map(collision_map)

        print('Printing current grid (occupied positions)')
        print(collision_map)

        return collision_map

