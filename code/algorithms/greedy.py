from enum import Enum
import random
import math
import copy

from code.algorithms.algorithm import Algorithm
from code.classes.score import Score

class Greedy(Algorithm):
    '''
    This is the greedy algorithm, written by Simon Antonides. It bases itself on version 2 of the Technical Description.
    
    '''
    def __init__(self, board, max_state_cache_size = 3):
        '''
        Parameters
        ----------
        board : Board
            the initial state of a Rush Hour board
        max_state_cache_size : int
            the maximum of unavailable prior states to progress to (default = 3)
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
        # print('amount_of_moves', len(moves))
        # return self.board, True
        best_score = 0 # self.score.calculate_value(self.board)
        best_moves = []

        worst_score = 0
        worst_moves = []

        for move in moves:
            if move.__repr__() not in self.state_cache:
                score = self.score.calculate_value(move)
                self.visited_states += 1
                # print(f'Level {len(self.states)} node: {score}')
                
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
        
        # print(best_moves)
        if len(self.states) == 0 or (len(best_moves) == 0 and len(worst_moves) == 0):
            return self.board, False
            
        elif len(best_moves) == 0 and len(worst_moves) != 0:
            best_moves = worst_moves
        if len(best_moves) == 1:
            self.board = best_moves[0]
        else:
            # print(best_moves)
            random_move = random.randint(0, len(best_moves) - 1)
            self.board = best_moves[random_move]
            # print('SM', self.score.calculate_value(self.board))

        if len(self.state_cache) >= self.max_state_cache_size:
            self.state_cache.pop()

        self.state_cache.append(self.board.repr())
        self.states.append(copy.deepcopy(self.board))
        # print('Chosen board:', self.score.calculate_value(self.board), self.board.repr(), self.board.get_amount_of_states())
        return self.board, False
        
        
    def get_name(self):
        '''
        Get name of the algorithm to save CSV-file
        
        Output
        ------
        name : str
            name of the algorithm
        '''
        return f'Greedy_VisitedStates{self.visited_states}'