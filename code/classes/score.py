

class Score:
    '''
    Creates a score for the board

    Attribute
    ---------    
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
    def __init__(self, score_positive_component_exponent_base = 2, score_positive_component_maximum_exponent = 8, score_positive_component_minimum_exponent = 5, score_positive_component_calculate_possible_position = True, score_negative_component_red_car_only_first = False, score_negative_component_exponent_base = 2, score_negative_component_maximum_exponent = 4, score_negative_component_amount_of_levels = 4):
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


    
    def calculate_value(self, board):
        '''
        Calculates current value of board according to Greedy scoring.

        Output
        ------
        score : int
          A negative or positive number of the score of the current board
        '''
        self.board = board
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
