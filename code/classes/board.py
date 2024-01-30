import pandas as pd
from math import ceil, log
import numpy as np
import copy

from code.classes.car import Car 

class Board:  
    '''
    Creates a board for the game Rush Hour

    Attribute
    ---------
    input_file: CSV
        The file with information about the board 
    car_csv : 
        Parsed CSV of cars
    size : int
        The size of the board 
    exit_row: int
        Indicates where an opening should be in the board for the red car to leave
    cars : dict
        A dict with all the cars that need to be placed on the board 
    moves : list
        Stores the made moves 
    archive : set 
        A set with all the possible following states of the current state
    ''' 
    def __init__(self, input_file, car_csv):
    
        start = input_file.find('hour') + len('hour')
        end = input_file.find('x', start)

        self.size = int(input_file[start:end].strip())
        self.cars = {}
        self.init_cars(car_csv)
        self.init_empty_collision_map()
        self.exit_row = ceil(self.size / 2)
        self.moves = []
        self.archive = set()

    
    def record_move(self, car_id, step):
        '''
        Appends a tuple of made moves and id of a car to a list 

        Parameters
        ----------
        car_id = str
            The id of the object car 
        step = int
            The move the car makes on the board 
        '''
        self.moves.append((car_id,step))

    def save_moves(self, output_filename):
        '''
        Exports the made moves to a csv file 

        Parameters
        ----------
        output_filename : str 
            the name + place where the file is being saved 
        '''
        df = pd.DataFrame(self.moves, columns=['car', 'move']) 
        
        df.to_csv(output_filename, index=False)

    def get_amount_of_moves(self):
        '''
        Gets the amount of moves the current board state has made to arrive at the current state

        Output
        ------
        amount_of_moves : int
        '''
        return len(self.moves)

    def get_amount_of_states(self):
        '''
        Gets the amount of states the current board has made to arrive at the current state. It uses the self.archive to determine this

        Output
        ------
        amount_of_states : int
        '''
        return len(self.archive)
    
    def init_cars(self, csv):
        '''
        Initializes all cars. This adds them to the board object in self.cars and to self.collision_map
    
        Parameters
        ----------
        csv : Dataframe
            Parsed CSV of cars in board
        '''
        for index, row in csv.iterrows():
            car = Car(row.car, row.orientation, row.col, row.row, row.length)
            self.cars[row.car] = car
            self.collision_map = car.update_collision_map(self.collision_map)

            if row.car == 'X':
                self.red_car = car

    def get_car(self, number_or_id):
        '''
        This function retrieves the car by number or by character(s). Returns None if the car can not be found

        Parameters
        ----------
        number_or_id : int or str
            A number as index (from 0 to length of list of self.cars) OR a char (for example 'X' or 'A')
        '''
        if isinstance(number_or_id, int) and len(list(self.cars.keys())) < number_or_id:
            return self.cars[list(self.cars.keys())[number_or_id]]
        elif number_or_id in self.cars:
            return self.cars[number_or_id]
        
        return None

    def get_collision_map_slice_and_start_pos(self, car):
        '''
        Retrieves the collision map slice upon which a car resides

        Parameters
        ----------
        car : Car 
            Used to make the slice

        Output
        ------
        collision_map_slice : np.chararray 
            The slice of self.collision_map on which the car resides
        start_pos : int
            The position of the current car
        '''
        if car.orientation == 'H':
            collision_map_slice = self.collision_map[car.row]
        else:
            collision_map_slice = self.collision_map[:,car.column]

        start_pos = car.get_pos()
        return (collision_map_slice, start_pos)

    def move(self, car, steps, execute=True):
        '''
        Moves a car in steps direction

        Parameters
        ----------
        car : Car
          The car that gets moved
        steps : int
          A number between -board_size and board_size
        execute : bool 
            Execute the move (default: False)

        Output
        ------
        success : boolean
            - True if move is made succesfully 
            - False if move is not possible
        '''
        if steps == 0:
            return False
        
        (collision_map_slice, start_pos) = self.get_collision_map_slice_and_start_pos(car)

        if steps > 0:
            end_pos = start_pos + car.length + steps
        else:
            start_pos += steps
            start_pos = max(0, start_pos)
            end_pos = start_pos + abs(steps) + car.length
         
        end_pos = min(end_pos, len(collision_map_slice))

        replace_slice = collision_map_slice[start_pos:end_pos]
        replacable_tf = replace_slice != b''

        if replacable_tf.sum() == car.length and replace_slice.shape[0] != car.length:
            if execute:
                replace_slice = np.flip(replace_slice)

                if car.orientation == 'H':
                    self.collision_map[car.row][start_pos:end_pos] = replace_slice
                    car.column += steps
                else:
                    self.collision_map[:,car.column][start_pos:end_pos]  = replace_slice
                    car.row += steps
        
                self.archive.add(self.__repr__())
                self.record_move(car.id, steps)

            return True

        return False

    def get_moves(self, car=None):
        '''
        Get all possible moves for the current state

        Parameters
        ----------
        car : Car
            show only the possible moves for this car (default = None)

        Output
        ------
        moves: list of tuples
            (car.id, steps)
        '''
        moves = []
        if car == None:
            cars = self.cars 
        else:
            cars = [car.id]

        for car in cars:
            i = -1
            while i <= 1:
                possible = True
                steps = 0
                while possible and abs(steps) < self.size:
                    steps += 1 * i
                    move_possible = self.move(self.cars[car], steps, False)
                    if move_possible:
                        moves.append((self.cars[car].id, steps))
                    else:
                        possible = False
                i += 2

        return moves

    def get_states(self, car=None):
        '''
        Get all possible states for the current state

        Parameters
        ----------
        car : Car
          Show only the possible moves for this car

        Output
        ------
        states : list of Board
            Board-object with the executed move
        '''
        board_states = []

        if car == None:
            cars = self.cars 
        else:
            cars = [car.id]

        for car in cars:
            i = -1
            while i <= 1:
                possible = True
                steps = 0
                while possible and abs(steps) < self.size:
                    steps += 1 * i
                    move_possible = self.move(self.cars[car], steps, False)
                    if move_possible:
                        new_state = copy.deepcopy(self)
                        new_state.move(new_state.cars[car], steps)
                        board_states.append(new_state)
                    else:
                        possible = False
                i += 2
        return board_states

    def init_empty_collision_map(self):
        '''
        Initializes an empty collision map
        '''
        
        # Create bounds for top, bottom and and sides        
        row_bound =  np.chararray((1, self.size), itemsize=2) 
        row_bound[:] = '-'

        column_bound = np.chararray((self.size + 2, 1), itemsize=2)  
        column_bound[:] = '-'


        # Create empty collision map
        self.collision_map = np.chararray((self.size, self.size), itemsize=2)
        self.collision_map[:] = ''

        self.collision_map = np.vstack((row_bound, self.collision_map, row_bound))
        self.collision_map = np.hstack((column_bound, self.collision_map, column_bound))

    def solve(self, execute=True):
        '''
        Looks if the board is solvable

        Paramters
        ---------
        execute : bool
            execute the solve (default = True)
        
        Output
        ------
        success : bool 
        '''
        return self.move(self.red_car, self.size - self.red_car.column - 1, execute=execute)

    def repr(self):
        '''
        This function uses a hash-function to represent a state. This is used for comparing states quickly to determine whether to examine a state

        Output
        ------
        repr : int
          A number (negative or positive)
        '''
        return hash(str(self.collision_map))
    def __repr__(self):
        '''
        This function uses a hash-function to represent a state. This is used for comparing states quickly to determine whether to examine a state

        Output
        ------
        repr : str
          A number (negative or positive) formatted as string
        '''
        return str(self.repr())