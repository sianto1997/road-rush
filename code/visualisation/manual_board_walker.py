from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
from code.classes.score import Score

class ManualBoardWalker(Algorithm):
    '''
    This class is being used to walk on a board manually (Only used for visualization purposes)

    Attributes
    ----------
    board : Board
        The current board state
    score : Score  
        Score class
    i : int
        Iterator
    cars : list of Car
        A manual list of cars that need to be moved
    moves : list of int
        A manual list of moves (min - board.size, max + board.size)
    moves2 : list of Board
        All possible states possible from initial board state 
    '''
    def __init__(self, board : Board):
        '''
        Parameters
        ----------
        board : Board
            The initial board state
        '''
        self.board = board
        self.score = Score()
        self.i = 0
        self.cars = [
            # board.get_car_by_index(4),
            # board.get_car_by_index(0),
            # board.get_car_by_index(2)
            ]
        self.moves = [
            -3,
            1,
            2
            ]
        
        self.moves2 = self.board.get_states()
        print(f'start {self.score.calculate_value(self.board)}')

    def run(self):
        '''
        Run one iteration of the manual board walker
        
        Output
        ------
        board : Board
            Current state of Rush Hour board
        solved : bool or None 
            - False : indicating no solution is found yet (all but last iteration)
            - None: : no solution is found at all (last iteration)
        '''
        # Run manual moves if available
        if self.i < len(self.cars):
            car = self.cars[self.i]
            move = self.moves[self.i]
            print(self.board.move(car, move))

            self.i += 1
            return self.board, False
        # Run moves possible from begin state
        elif self.i < len(self.moves2):
            self.board = self.moves2.pop()
            self.i += 1
            return self.board, False
        # Always quit and do not save, even if solution is found
        else:
            return self.board, None

    def get_name(self):
        '''
        Get name of the algorithm to save CSV-file
        
        Output
        ------
        name : str
            Name of the algorithm
        '''
        return 'ManualBoardWalker'