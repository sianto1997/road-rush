import matplotlib.pyplot as plt
import pandas as pd
from Car import Car 

class Board:
    def __init__(self, input_file):
        start = input_file.find('hour') + len('hour')
        end = input_file.find('x', start)
        self.size = int(input_file[start:end].strip())
        self.exit_row = self.size // 2
        self.cars = []
        print(self.size, self.exit_row)


    def add_cars(self, csv):
        for index, row in csv.iterrows():
            car = Car(row.car, row.orientation, row.col, row.row, row.length)
            self.cars.append(car)
    
    def visualize(self):
        board = plt.figure(figsize=[6,6])
        board.patch.set_facecolor((1,1,.8))
        ax = board.add_subplot(111)
        for x in range(13):
            ax.plot([x, x], [0,12], 'k')
        for y in range(12):
            ax.plot([0, 12], [y,y], 'k')
        ax.set_position([0,0,1,1])
        ax.set_axis_off()
        ax.set_xlim(-1,13)
        ax.set_ylim(-1,13)
        plt.savefig(board)
        

        