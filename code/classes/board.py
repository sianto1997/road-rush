import matplotlib.pyplot as plt
import pandas as pd
from car import Car 
from math import ceil
import numpy as np

class Board:   
    def __init__(self, input_file, car_csv, visualize=False):
        """
        Creates a board for the game Rush Hour.

        Input:
        - input_file = CSV, the file with information about the board 
        - car_csv = parsed CSV of cars
        - visualize = show visualization (do not display by default)
        """ 
        self.visualize = visualize

        # get position of 'hour' in title of input file
        start = input_file.find('hour') + len('hour')
        
        # get position of 'x' in title of input file, starting from position 'hour'
        end = input_file.find('x', start)
        
        # extract substring between 'hour' and 'x', convert to  integer and remove whitespaces
        self.size = int(input_file[start:end].strip())

        # devides the self.size by 2, if answer is float then number is rounded upwards 
        self.exit_row = ceil(self.size / 2)
        self.cars = []
        self.red_car = None
        self.init_cars(car_csv)

        self.moves = []

        if (visualize):
            self.init_visualization()

    def record_move(self, car_id, step):
        """
        Appends a tuple of made moves and id of a car to a list 

        Input:
        - car_id = str, the id of the object car 
        - step = int, the move the car makes on the board 
        """
        self.moves.append((car_id,step))

    def save_moves(self, output_filename):
        """ 
        Exports the made moves to a csv file 

        Input:
        - output_filename = str, the name + place where the file is being saved 
        """
        df = pd.DataFrame(self.moves, columns=['car', 'move']) 
        
        df.to_csv(output_filename, index=False)

    def get_amount_of_moves(self):
        return len(self.moves)

    def init_cars(self, csv):
        """
            Initializes all cars
        
            Input:
            csv = Dataframe, parsed CSV of cars in board
        """
        # loops over the index and rows of the given dataframe 
        for index, row in csv.iterrows():

            # creates the car object with the information of the dataframe
            car = Car(row.car, row.orientation, row.col, row.row, row.length)
    
            # appends the object car to the list self.cars 
            self.cars.append(car)

            # Saving the red car to later check for finish
            if row.car == 'X':
                self.red_car = car
    
    def init_visualization(self):
        """
        Initializes the board so that only one display is created
        """
        # give the range to the figure
        self.canvas = plt.figure(figsize=[self.size + 0.5, self.size + 0.5])

        # makes the background colour of the figure gray
        self.canvas.patch.set_facecolor('gray')

        # creates the grid place
        self.ax = self.canvas.add_subplot()


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
        # Pause to be able to show the visualization
        plt.pause(0.0001)

        self.ax.cla()

    def close_visualization(self):
        if self.visualize:
            plt.close(self.canvas)

    def move(self, car, steps):
        """
        Moves a car in steps direction
        Input:
        - car (Car-object)
        - steps (a number between -board_size and board_size)
        Output:
        - success (True or False)
        """
        collision_map = self.get_collision_map()
        # print(car.id, steps)
        
        if car.orientation == 'H':
            collision_map_slice = collision_map[car.row]
            start_pos = car.column
        else:
            collision_map_slice = collision_map[:,car.column]
            start_pos = car.row

        offset = 0
        if steps > 0:
            offset = car.length
        else:
            offset = steps

        start_pos = max(0, start_pos + offset)
        end_pos = min(start_pos+abs(steps), len(collision_map_slice))
        target_area = collision_map_slice[start_pos:end_pos] == 1
        
        if not target_area.any() and len(target_area) > 0:
            if car.orientation == 'H':
                car.column += steps
            else:
                car.row += steps
            
            # print(f'Move of car {car.id} ({car.orientation}) successful: {steps}')
            self.draw()
            self.record_move(car.id, steps)
            return True

        # print(f'Move of car {car.id} ({car.orientation}) was unsuccessful: {steps}')
        return False
        

    def get_collision_map(self):
        """
        Gets the current collision map

        TODO for Simon: make more efficient by only creating map at init, and edit at move()
        """

        # Create bounds for top, bottom and and sides
        row_bound = np.ones((1, self.size))
        column_bound = np.ones((self.size + 2, 1))

        # Create empty collision map
        collision_map = np.zeros((self.size, self.size))

        collision_map = np.vstack((row_bound, collision_map, row_bound))
        collision_map = np.hstack((column_bound, collision_map, column_bound))

        # Unblock exit row
        collision_map[self.exit_row][self.size+1] = 0
        
        # Loop through all cars and get their position
        for car in self.cars:
            collision_map = car.update_collision_map(collision_map)

        # Debug
        # print('Printing current grid (occupied positions)')
        # print(collision_map)

        return collision_map

    def finish(self):
        """
        """
        # Discuss with TA: check50 reports car hit a wall where there is no wall
        if self.move(self.red_car, self.size - self.red_car.column - 1):
            moves = len(self.moves)
            print(f'Game is finished! It took {moves} moves')
            return True
        
        return False