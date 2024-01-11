import matplotlib.pyplot as plt
import pandas as pd
from car import Car 
from math import ceil
import numpy as np
import time

class Board:
    def __init__(self, input_file):
        start = input_file.find('hour') + len('hour')
        end = input_file.find('x', start)
        self.size = int(input_file[start:end].strip())
        self.exit_row = ceil(self.size / 2)
        self.cars = []
        print(self.size, self.exit_row)


    def add_cars(self, csv):
        for index, row in csv.iterrows():
            car = Car(row.car, row.orientation, row.col, row.row, row.length)
            self.cars.append(car)
            if car.id == 'X':
                self.red_car = car


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
      
        # plt.show()
        plt.draw()
        plt.pause(0.01)

        ax.cla()



    def try_move(self, car, steps):
        time.sleep(1.5)

        grid = self.map_grid()
        step_size = 1
        start = 1
        if steps < 0:
            step_size = -1
            start = -1

        for movement in range(start, steps + 1, step_size):
            # if 0 >= car.begin_and_end >= self.size 
            if not car.try_move(grid, movement):
                print(f'Move of car {car.id} ({car.orientation}) unsuccessful at step {movement}, goal was {steps}')
                return False

        
        car.move(steps)
        self.visualize_board()

        return True

    def map_grid(self):
        grid = np.zeros((self.size, self.size))
        for car in self.cars:
            grid = car.update_grid(grid)

        return grid

    def start_experiment(self):
        # self.try_move(self.cars[0], -1)
        
        
        # self.try_move(self.cars[1], -1)

           
        
        # self.try_move(self.cars[2], 1)

        self.try_move(self.cars[-4], -1)
        self.try_move(self.cars[-5], 2)
