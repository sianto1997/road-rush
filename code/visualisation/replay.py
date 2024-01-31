import pandas as pd
from code.algorithms.algorithm import Algorithm
from code.classes.board import Board

class Replay(Algorithm):
    '''
    This class is used to replay results

    Attributes
    ----------
    board : Board
        The current board state
    i : int
        The current iteration
    moves : pd.DataFrame
        The moves to replay
    '''
    def __init__(self, board : Board, input : str):
        '''
        Parameters
        ----------
        board : Board
            The initial board state
        input : str
            The moves to replay
        '''
        self.board = board
        self.i = 0
        self.moves = pd.read_csv(input) 
        self.size = len(self.moves)
        # print(self.moves, self.size)

    def run(self):
        if self.i < self.size:
            self.board.move(self.board.get_car_by_id(self.moves.iloc[self.i].car), self.moves.iloc[self.i].move)

            self.i += 1
            return self.board, False
        else:
            # Quit
            return self.board, None

    def get_name(self):
        return 'Replay'