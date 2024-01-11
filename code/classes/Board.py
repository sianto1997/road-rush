import matplotlib.pyplot as plt
import pandas as pd
from Car import Car 
from math import ceil

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
    
    def visualize(self):
        board = plt.figure(figsize=[self.size+0.5,self.size+0.5])
        board.patch.set_facecolor('gray')
        ax = board.add_subplot()
        ax.invert_yaxis()
        for x in range(1,self.size+1):
            ax.plot([x, x], [1,self.size+1], 'k')
        ax.plot([self.size+1, self.size+1], [1,self.exit_row], 'k')
        ax.plot([self.size+1, self.size+1], [self.exit_row+1,self.size+1], 'k')
        for y in range(1,self.size+2):
            ax.plot([1, self.size+1], [y,y], 'k')
        ax.set_position([0,0,1,1])
        ax.set_axis_off()
      
        plt.show()

        

        