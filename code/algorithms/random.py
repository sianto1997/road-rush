from enum import Enum
import random

from code.algorithms.algorithm import Algorithm

class MoveMethod(Enum):
    '''
    The MoveMethods determine how far a car can move in one move.
    
    RandomAll can move between and including - board_size to and including + board_size
    RandomOne can move - 1 or + 1
    RandomTwo can move between and including - 2 or + 2
    RandomThree can move between and including - 3 or + 3
    '''
    RandomAll = 0
    RandomOne = 1
    RandomTwo = 2
    RandomThree = 3

class Random(Algorithm):
    '''
    This is the Random algorithm
    
    Attributes
    ----------
    board : Board
        The current state of the Rush Hour board
    move_method : MoveMethod
        The MoveMethod of the current experiment
    '''
    def __init__(self, board, move_method = MoveMethod.RandomAll):
        '''
        Parameters
        ----------
        board : Board
            The initial state of a Rush Hour board
        move_method : int
            The MoveMethod to be used in the current experiment (default = MoveMethod.RandomAll)
        '''
        self.board = board
        self.move_method = move_method
            
    def run(self):
        '''
        Run one iteration of Random algorithm
        
        Output
        ------
        board : Board
            Current state of Rush Hour board
        solved : bool
            - True : Indicating a solution is found
            - False : Indicating no solution is found yet
        '''
        car_index = random.randint(0, len(self.board.cars) - 1)

        if MoveMethod(self.move_method) == MoveMethod.RandomAll:
            steps = random.randint(-self.board.size,self.board.size)
        else:
            steps = random.randint(-self.move_method,self.move_method)

        self.board.move(self.board.get_car(car_index), steps)

        return self.board, self.board.solve()

    def get_name(self):
        '''
        Get name of the algorithm to save CSV-file
        
        Output
        ------
        name : str
            Name of the algorithm
        '''
        return MoveMethod(self.move_method).name