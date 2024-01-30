from enum import Enum
import random
import copy

from code.algorithms.algorithm import Algorithm
from code.classes.score import Score

class Greedy(Algorithm):
    '''
    This is the Greedy algorithm. It bases itself on version 2 of the Technical Description
    '''
    def __init__(self, board, max_state_cache_size = 3):
        '''
        Parameters
        ----------
        board : Board
            The initial state of a Rush Hour board
        max_state_cache_size : int
            The maximum of unavailable prior states to progress to (default = 3)
        '''
        self.score = Score()
        self.board = board
        self.best_state = self.board
        self.best_score = self.score.calculate_value(self.board)
        
        self.states = [copy.deepcopy(self.board)]

        self.archive = set()
        self.archive.add(self.board.repr())

        self.visited_states = 0

        self.state_cache = list()
        self.state_cache.append(self.board.repr())

        # The state cache is created to avoid ending in an infinite loop with the same states
        self.max_state_cache_size = max_state_cache_size


        print(f'Start score = {self.best_score} {self.board.repr()}')
        
    def run(self):

        solvable = self.board.solve()
        if solvable:
            return self.board, solvable
        moves = self.board.get_states()
        best_score = 0
        best_moves = []

        worst_score = 0
        worst_moves = []

        for move in moves:
            if move.__repr__() not in self.state_cache:
                score = self.score.calculate_value(move)
                self.visited_states += 1
                
                if score > best_score:
                    best_moves = [move]
                    best_score = score
                elif score == best_score:
                    best_moves.append(move)
                
                if score < worst_score:
                    worst_score = score
                    worst_moves = [move]
                elif score == worst_score:
                    worst_moves.append(move)
        
        if len(self.states) == 0 or (len(best_moves) == 0 and len(worst_moves) == 0):
            return self.board, False
            
        elif len(best_moves) == 0 and len(worst_moves) != 0:
            best_moves = worst_moves
        if len(best_moves) == 1:
            self.board = best_moves[0]
        else:
            random_move = random.randint(0, len(best_moves) - 1)
            self.board = best_moves[random_move]

        if len(self.state_cache) >= self.max_state_cache_size:
            self.state_cache.pop()

        self.state_cache.append(self.board.repr())
        self.states.append(copy.deepcopy(self.board))
        return self.board, False
        
        
    def get_name(self):
        '''
        Get name of the algorithm to save CSV-file
        
        Output
        ------
        name : str
            Name of the algorithm
        '''
        return f'Greedy_VisitedStates{self.visited_states}'