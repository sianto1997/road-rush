import matplotlib.pyplot as plt
import pandas as pd
from car import Car 
from math import ceil
import numpy as np

class Board:   
    def __init__(self, input_file):
        """
        Creates a board for the game Rush Hour
        - input_file = CSV, the file with information about the board 
        """ 
        
        start = input_file.find('hour') + len('hour')
        end = input_file.find('x', start)
        self.size = int(input_file[start:end].strip())
        self.exit_row = ceil(self.size / 2)
        self.cars = []
        print(self.size, self.exit_row)


    def add_cars(self, csv):

        # loops over the index and rows of the given dataframe 
        for index, row in csv.iterrows():

            # creates the car obejct with the information of the dataframe
            car = Car(row.car, row.orientation, row.col, row.row, row.length)
    
            # appends the object car to the list self.cars 
            self.cars.append(car)


        print(self.map_grid())
    
    def visualize_board(self):
        """
        Visualizes the object board
        """
        # give the range to the figure
        board = plt.figure(figsize=[self.size+0.5,self.size+0.5])

        # makes the background colour of the figure gray
        board.patch.set_facecolor('gray')

        # creates the grid place
        ax = board.add_subplot()

        # inverts the values of the y-axis
        ax.invert_yaxis()

        # loops over the values of the x-axis
        for x in range(1,self.size+1):
            
            # makes a black line on the places of the x in a particular range 
            ax.plot([x, x], [1,self.size+1], 'k')
        
        # makes the exit row line
        ax.plot([self.size+1, self.size+1], [1,self.exit_row], 'k')
        ax.plot([self.size+1, self.size+1], [self.exit_row+1,self.size+1], 'k')

        # loops over the values of y-axis
        for y in range(1,self.size+2):

            # makes a black line on the places of the y in a particular range
            ax.plot([1, self.size+1], [y,y], 'k')
        
        # create marges around the grid 
        ax.set_position([0,0,1,1])

        # deletes the axis numbers 
        ax.set_axis_off()

        for car in self.cars:
            car.visualize_car(ax)
      
        plt.show()

    def move_possible(self, start_location, car_size, steps):
        return False 

    def map_grid(self):
        grid = np.zeros((self.size, self.size))
        for car in self.cars:
            grid = car.update_grid(grid)

        return grid