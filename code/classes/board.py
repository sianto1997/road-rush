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
    
    score_positive_component_exponent_base : int
        The base of the exponent used in positive component of score (Default is 2) 
    score_positive_component_maximum_exponent : int
        The maximum exponent of 2 for the score of the positive component (default is 8, which translates to 256 as max value)
    score_positive_component_minimum_exponent : int
        The minimum exponent of 2 for the score to no longer calculate as part of the positive component (default is 5, which translated to 32 as min value)
    score_positive_component_calculate_possible_position : bool
        Count the potential position of the red car in the positive component of the score (Default True)
    
    score_negative_component_red_car_only_first : bool
        Look only at the first obstruction for determining negative component (Default True)
    score_negative_component_exponent_base : int 
        The base of the exponent used in negative component of score (Default is 2)
    score_negative_component_maximum_exponent : int
        The maximum exponent of 2 for the score of the negative component (default is 4, which translates to 16 as max value)
    score_negative_component_amount_of_levels : int
        The amount of levels deep to explore obstructions as part of the negative component, the score halves each level (Default is 3)
    ''' 
    def __init__(self, input_file, car_csv, score_positive_component_exponent_base = 2, score_positive_component_maximum_exponent = 8, score_positive_component_minimum_exponent = 5, score_positive_component_calculate_possible_position = True, score_negative_component_red_car_only_first = False, score_negative_component_exponent_base = 2, score_negative_component_maximum_exponent = 4, score_negative_component_amount_of_levels = 4):
    
        start = input_file.find('hour') + len('hour')
        end = input_file.find('x', start)

        self.size = int(input_file[start:end].strip())
        self.cars = {}
        self.init_cars(car_csv)
        self.init_empty_collision_map()
        self.exit_row = ceil(self.size / 2)
        self.moves = []
        self.archive = set()

        self.score_positive_component_exponent_base = score_positive_component_exponent_base
        self.score_positive_component_maximum_exponent = score_positive_component_maximum_exponent
        self.score_positive_component_minimum_exponent = score_positive_component_minimum_exponent
        self.score_positive_component_calculate_possible_position = score_positive_component_calculate_possible_position
        self.score_positive_component_minimum = self.score_positive_component_exponent_base ** self.score_positive_component_minimum_exponent
        
        self.score_negative_component_red_car_only_first = score_negative_component_red_car_only_first
        self.score_negative_component_exponent_base = score_negative_component_exponent_base
        self.score_negative_component_maximum_exponent = score_negative_component_maximum_exponent
        self.score_negative_component_amount_of_levels = score_negative_component_amount_of_levels
        self.score_negative_component_diff_amount_of_levels_maximum = self.score_negative_component_maximum_exponent - self.score_negative_component_amount_of_levels + 1

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
            Show only the possible moves for this car (default = None)

        Output
        ------
        List of tuples : 
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
        List of states :
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
        execute : bool, optional
          Execute the solve
        
        Output
        ------
        boolean: Success
        '''
        return self.move(self.red_car, self.size - self.red_car.column - 1, execute=execute)

    def repr(self):
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
    
    def calculate_value(self):
        '''
        Calculates current value of board according to Greedy scoring.

        Output
        ------
        score : int
          A negative or positive number of the score of the current board
        '''
        positive_score = self.calculate_positive_component_of_score()

        negative_score = self.calculate_negative_component_of_score()

        score = positive_score + negative_score

        return score
    
    def calculate_positive_component_of_score(self):
        '''
        This function calculates the positive component of the score.

        Output
        ------
        score : int
          A number between 0 and 256 (solved board). The best score without a solved board is 128
        '''
        score = 0

        max_pos = self.size - 1

        highest_possible_pos = self.red_car.get_pos()
        
        if self.score_positive_component_calculate_possible_position:
            possible_moves = self.get_states(self.red_car)
            for move in possible_moves:
                red_car_pos = move.red_car.get_pos()
                if red_car_pos > highest_possible_pos:
                    highest_possible_pos = red_car_pos


        possible_positive_score = self.score_positive_component_exponent_base ** (self.score_positive_component_maximum_exponent - (max_pos - highest_possible_pos))
        if possible_positive_score >= self.score_positive_component_minimum:
            score += possible_positive_score

        return score
    
    def calculate_negative_component_of_score(self):
        '''
        This function is used to calculate the negative component of the score
        '''
        score = 0

        obstructors = []

        # All results of the red car (only looks forward for the red car)
        if self.score_negative_component_red_car_only_first:
            obstructors_of_red_car = self.obstructed_by(self.red_car, True, False)
        else:
            obstructors_of_red_car = self.obstructed_by(self.red_car, True, True)

        if obstructors_of_red_car != None:
            obstructors.extend(obstructors_of_red_car)

            for (obstructor, position_to_clear) in obstructors:
                score += self.calculate_negative_component_of_score_recursive(self.score_negative_component_amount_of_levels - 1, obstructor, position_to_clear, self.red_car, set([self.red_car.id, obstructor.id]))

        return score

    def calculate_negative_component_of_score_recursive(self, levels_to_go, obstructor, position_to_clear, obstructed, passed_obstructions):
        '''
        The recursive function helping calculate the negative component of the score

        Parameters
        ------
        levels_to_go : int
          Lowers every step, stops when the level reaches 0.
        current_obstruction : Car
          The car obstructing the previous car.
        position_to_clear : int
          The position we want cleared
        source_of_obstruction
        - passed_obstructions (list of str): The list of cars (identified by car.id) already passed (checked to avoid double counting the scores).
        '''
        score = 0
        if levels_to_go >= 0: 
            clearance_multiplier = 1
            can_be_cleared = self.obstruction_can_be_cleared(obstructor, position_to_clear, obstructed)

            if not can_be_cleared:
                clearance_multiplier = -1
                add_to_current =  (self.score_negative_component_exponent_base ** (levels_to_go + self.score_negative_component_diff_amount_of_levels_maximum) * clearance_multiplier)
            else:
                add_to_current =  (self.score_negative_component_exponent_base ** (self.score_negative_component_amount_of_levels - levels_to_go) * clearance_multiplier)
            
            score += add_to_current
            
            if levels_to_go <= self.score_negative_component_amount_of_levels and levels_to_go > 0 and not can_be_cleared:
                obstructions = []

                forward = self.obstructed_by(obstructor, True, self.score_negative_component_red_car_only_first)
                obstructed = True

                if forward != None:
                    obstructions.append(forward[0])
        
                backward = self.obstructed_by(obstructor, False, self.score_negative_component_red_car_only_first)

                if backward != None:
                    obstructions.append(backward[0])

                if len(obstructions) == 2:
                    child_scores = []
                    while len(obstructions) > 0:
                        (obstruction, position_to_clear) = obstructions.pop()

                        if obstruction.id not in passed_obstructions:
                            passed_obstructions.add(obstruction.id)
                            child_scores.append(self.calculate_negative_component_of_score_recursive(levels_to_go - 1, obstruction, position_to_clear, obstructor, passed_obstructions))
                    
                    if len(child_scores) > 0:
                        if max(child_scores) > 0:
                            score += max(child_scores)
                        else:
                            score += sum(child_scores)

                else:
                    score += self.score_negative_component_exponent_base ** ((levels_to_go - 1) + self.score_negative_component_diff_amount_of_levels_maximum)
            
        return score

    def obstructed_by(self, car, forwards=True, only_first=True):
        '''
        This function figures out what blocks the car in the direction forwards (or backwards) and returns the car(s) that are obstruction it
        If there are no obstructions (only a wall) than the function returns None

        Parameters
        ----------
        car : Car
            The car that has or does not have obstructions
        forwards : bool
          Look forwards (Default is True)
        only_first : bool
          Only return first obstruction. For the red_car all obstructions are returned (Default is True)
        
        Output
        ------
        cars : Car
          A list of 1 or more cars , dependant on only_first being True or False
        '''
        (collision_map_slice, start_pos) = self.get_collision_map_slice_and_start_pos(car)
    
        obstructed = False
        step_size = - 1
        
        i = start_pos - 1
        
        if forwards:
            step_size = 1
            i += car.length + 1
    
        results = []

        while not obstructed:
            possible_obstruction = collision_map_slice[i].decode()

            if possible_obstruction == '-':
                obstructed = True
            elif not possible_obstruction == '':
                if only_first:
                    obstructed = True
                results.append((self.get_car(possible_obstruction), car.get_pos(True)))
            
            i += step_size

        if len(results) >= 1:
            if only_first:
                return [results[0]]
            return results
        
        return None
  
    def obstruction_can_be_cleared(self, obstructor, position_to_clear, obstructed):
        '''
        Checks whether an obstruction can be cleared by the car in question

        Parameters
        ----------
        obstructor : Car
            The car we need, to know if it can unblock the position_to_clear
        position_to_clear : int
          A position that we want to clear
        obstructed : Car
          Used for determining the orientation of the two cars for comparing the right positions

        Output:
        can_be_cleared : boolean
          - True if it can be cleared
          - False if it cannot be cleared 
        '''

        if obstructor.orientation != obstructed.orientation:
            clear_pos_lower_than_or_equals = obstructed.get_pos(True) - obstructor.length
            clear_pos_higher_than_or_equals = position_to_clear + 1

        else:
            clear_pos_lower_than_or_equals = obstructed.get_pos() - obstructor.length
            clear_pos_higher_than_or_equals = position_to_clear + 1

        neg = -1
        while neg <= 1:
            for steps in range(1, self.size + 1):
                adjusted_pos = obstructor.get_pos() + steps * neg
                if adjusted_pos <= clear_pos_lower_than_or_equals or adjusted_pos >= clear_pos_higher_than_or_equals:
                    if self.move(obstructor, steps * neg, False):
                        return True
                    else:
                        break
            neg += 2

        return False