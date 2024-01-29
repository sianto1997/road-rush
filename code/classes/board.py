import matplotlib.pyplot as plt
import pandas as pd
from code.classes.car import Car 
from math import ceil, log
import numpy as np
import copy

class Board:   
    def __init__(self, input_file, car_csv):
        '''
        Creates a board for the game Rush Hour.

        Input:
        - input_file = CSV, the file with information about the board 
        - car_csv = parsed CSV of cars
        '''

        # get position of 'hour' in title of input file
        start = input_file.find('hour') + len('hour')
        
        # get position of 'x' in title of input file, starting from position 'hour'
        end = input_file.find('x', start)
        
        # extract substring between 'hour' and 'x', convert to  integer and remove whitespaces
        self.size = int(input_file[start:end].strip())

        # devides the self.size by 2, if answer is float then number is rounded upwards 
        self.exit_row = ceil(self.size / 2)
        self.cars = {}
        self.red_car = None

        self.init_empty_collision_map()

        self.init_cars(car_csv)

        self.moves = []

        self.archive = set()

    def record_move(self, car_id, step):
        '''
        Appends a tuple of made moves and id of a car to a list 

        Input:
        - car_id = str, the id of the object car 
        - step = int, the move the car makes on the board 
        '''
        self.moves.append((car_id,step))

    def save_moves(self, output_filename):
        '''
        Exports the made moves to a csv file 

        Input:
        - output_filename = str, the name + place where the file is being saved 
        '''
        df = pd.DataFrame(self.moves, columns=['car', 'move']) 
        
        df.to_csv(output_filename, index=False)

    def get_amount_of_moves(self):
        return len(self.moves)

    def get_amount_of_states(self):
        return len(self.archive)
    
    def init_cars(self, csv):
        '''
            Initializes all cars
        
            Input:
            csv = Dataframe, parsed CSV of cars in board
        '''
        # loops over the index and rows of the given dataframe 
        for index, row in csv.iterrows():

            # creates the car object with the information of the dataframe
            car = Car(row.car, row.orientation, row.col, row.row, row.length)
    
            # appends the object car to the list self.cars 
            self.cars[row.car] = car

             # Loop through all cars and get their position
            self.collision_map = car.update_collision_map(self.collision_map)
            # print(self.collision_map)

            # Saving the red car to later check for finish
            if row.car == 'X':
                self.red_car = car

    def get_car(self, number_or_id):
        if isinstance(number_or_id, int):
            return self.cars[list(self.cars.keys())[number_or_id]]
        else:
            return self.cars[number_or_id]

    def get_collision_map_slice_and_start_pos(self, car):
        if car.orientation == 'H':
            collision_map_slice = self.collision_map[car.row]
            start_pos = car.column
        else:
            collision_map_slice = self.collision_map[:,car.column]
            start_pos = car.row
        return (collision_map_slice, start_pos)

    def move(self, car, steps, execute=True):
        '''
        Moves a car in steps direction

        Input:
        - car (Car): The car that gets moved
        - steps (int): A number between -board_size and board_size
        - execute (bool): Execute the move (default: False)
        Output:
        - success (True or False)
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
        # if not execute:
        #     print(car.id, car.orientation, car.column, car.row, steps, start_pos, end_pos)
        #     print(collision_map_slice, replace_slice, replacable_tf)

        if replacable_tf.sum() == car.length and replace_slice.shape[0] != car.length:
            if execute:
                replace_slice = np.flip(replace_slice)

                if car.orientation == 'H':
                    self.collision_map[car.row][start_pos:end_pos] = replace_slice
                    car.column += steps
                else:
                    self.collision_map[:,car.column][start_pos:end_pos]  = replace_slice
                    car.row += steps
                
                # print(f'Move of car {car.id} ({car.orientation}) successful: {steps}')
                # self.draw()
                self.archive.add(self.__repr__())
                self.record_move(car.id, steps)

            return True

        return False
        
    def get_moves(self, output_as_states=False, car=None):
        '''
        Get all possible moves for the current state. Discuss with TA about output as states.

        Input:
        - output_as_states (bool): Output the possible moves as new states. (disabled by default)
        - car (Car): Show only the possible moves for this car
        Output:
        - List of tuples (car.id, steps)
        OR
        - List of states (Board-object with the executed move)
        '''
        board_states = []
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
                        if output_as_states:
                            new_state = copy.deepcopy(self)
                            new_state.move(new_state.cars[car], steps)
                            board_states.append(new_state)
                        else:
                            moves.append((self.cars[car].id, steps))
                    else:
                        possible = False
                i += 2
        if output_as_states:
            return board_states

        return moves

    def init_empty_collision_map(self):
        '''
        Gets the current collision map
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

        Input:
        - execute (bool, optional): Execute the solve
        
        Output:
        - bool: Success
        '''
        if self.move(self.red_car, self.size - self.red_car.column - 1, execute=execute):
            moves = len(self.moves)
            # print(f'Game is finished! It took {moves} moves')
            return True
        
        return False

    def __repr__(self):
        # print(str(self.collision_map))
        return str(hash(str(self.collision_map)))
    
    def calculate_value(self):
        '''
        Calculates current value of board according to greedy scoring.
        '''
        pscore = 0

        # Positive component
        max_positive_score = 128
        positive_score_exponent = 2
        max_pos = self.size - 1

        highest_possible_pos = self.red_car.get_pos()

        possible_positive_score = positive_score_exponent ** (1 + log(max_positive_score, positive_score_exponent) - (max_pos - highest_possible_pos))
        
        if possible_positive_score >= max_positive_score / 4:
            pscore += possible_positive_score

        # print('Positive component', pscore)

        nscore = 0

        # Negative component
        obstructions = []
        # All results of the red car 
        obstructions_of_red_car = self.obstructed_by(self.red_car, True, False)

        # passed_obstructions = 

        if obstructions_of_red_car != None:
            obstructions.extend(obstructions_of_red_car)
            max_negative_score = 16

            # for (obstruction, position_to_clear) in obstructions:
            #     passed_obstructions.append(obstruction.id)

            level = 1
            for (obstruction, position_to_clear) in obstructions:
                nscore = self.score_recursive(nscore, max_negative_score, obstruction, level, position_to_clear, self.red_car, set([self.red_car.id, obstruction.id]))
            # print('Negative component', nscore)

        score = pscore + nscore

        # print('Total score', score)
        return score
    
    def score_recursive(self, current_score, add, current_obstruction, current_level, position_to_clear, source_obstruction, passed_obstructions):
        # print('a', add, current_obstruction)
        max_level = 3
        min_negative_score = 4
        # print('snscore', current_score)
        if add >= min_negative_score:

            # If an ostruction can be cleared (car can be moved out of the way) than the result is multiplied by -1 to result in a positive add. If not, the result will be multiplied by 1, which results in a negative add.
            clearance_multiplier = 1
            #current_obstruction != None and
            can_be_cleared = self.obstruction_can_be_cleared(current_obstruction, position_to_clear, source_obstruction)
            if not can_be_cleared or current_level == 1:
                clearance_multiplier = -1
            # print('cm', clearance_multiplier)
            add_to_current =  (add * clearance_multiplier)
            current_score += add_to_current
            # print(current_score)

            # print('na', new_add)
            new_add = add / 2

            # print(current_obstruction.id, add_to_current, can_be_cleared)
            # print(current_level, max_level)
            # print(current_level, max_level)
            if current_level <= max_level and new_add >= min_negative_score and not can_be_cleared:
                obstructions = []

                forward = self.obstructed_by(current_obstruction, True)

                if forward != None:
                    obstructions.append(forward)

                backward = self.obstructed_by(current_obstruction, False)

                if backward != None:
                    obstructions.append(backward)

                while len(obstructions) > 0:
                    (obstruction, position_to_clear) = obstructions.pop()
                    if obstruction.id not in passed_obstructions:
                        passed_obstructions.add(obstruction.id)
                        current_score = self.score_recursive(current_score, new_add, obstruction, current_level + 1, position_to_clear, current_obstruction, passed_obstructions)

        return current_score

    def obstructed_by(self, car, forwards=True, only_first=True):
        '''

        '''
        (collision_map_slice, start_pos) = self.get_collision_map_slice_and_start_pos(car)
        # print(collision_map_slice)
        obstructed = False
        step_size = - 1
        
        i = start_pos - 1
        

        # For forwards, adjust starting pos and step_size
        if forwards:
            step_size = 1
            i += car.length + 1
        # print(car.id, i, 'FF', forwards, step_size)
        results = []

        while not obstructed:
            possible_obstruction = collision_map_slice[i].decode()
            # print(i, possible_obstruction)

            if possible_obstruction == '-':
                obstructed = True
            elif not possible_obstruction == '':
                if only_first:
                    obstructed = True
                results.append((self.get_car(possible_obstruction), car.get_pos(True)))
            
            i += step_size

        if len(results) >= 1:
            if only_first:
                return results[0]
            return results
        
        return None
  
    def obstruction_can_be_cleared(self, car, position_to_clear, source):
        # print('ocbc_car', car, position_to_clear)
        if car.orientation != source.orientation:
            clear_pos_lower_than_or_equals = source.get_pos(True) - car.length
            clear_pos_higher_than_or_equals = position_to_clear + 1

        else:
            clear_pos_lower_than_or_equals = source.get_pos() - car.length
            clear_pos_higher_than_or_equals = position_to_clear + 1
        # print('ptc', position_to_clear, car.id)
        # print('cp1', clear_pos_lower_than_or_equals)
        # print('cp2', clear_pos_higher_than_or_equals)

        neg = -1
        while neg <= 1:
            for steps in range(1, self.size + 1):
                adjusted_pos = car.get_pos() + steps * neg
                # print('AP', adjusted_pos)
                if adjusted_pos <= clear_pos_lower_than_or_equals or adjusted_pos >= clear_pos_higher_than_or_equals:
                    if self.move(car, steps * neg, False):
                        return True
                    else:
                        break
            neg += 2

        return False