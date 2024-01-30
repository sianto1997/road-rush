from enum import Enum
import random
import math
import copy

from code.algorithms.algorithm import Algorithm

class GreedyRandom(Algorithm):
    '''
    This is a variation on the greedy algorithm using more random components
    
    Attributes
    ----------
    board : Board
        the current state of the Rush Hour board
    best_state : Board
        the best state until now
    best_score : int
        the score of the best state until now
    states : list of Board
        a stack to store states you still need to look into
    archive : set of int
        keeps track of the states which are already visited
    visited_states : int
        amount of states the algorithm did look at to find a solution
    state_cache : set of int
        the last N states (N = max_state_cache_size) used for determining whether a state can be visited
    max_state_cache_size : int
        the maximum amount of states in the state cache
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
        self.board = board
        self.best_state = self.board
        self.best_score = self.board.calculate_value()

        self.states = [copy.deepcopy(self.board)]

        self.archive = set()
        self.archive.add(self.board.repr())

        self.visited_states = 0

        # The state cache is created to avoid ending in an infinite loop with the same states
        self.state_cache = set()
        self.state_cache.add(self.board.repr())

        self.max_state_cache_size = max_state_cache_size
        
    def run(self):
        '''
        Run the Greedy DepthFirst algorithm until all possible states are visited
        
        Output
        ------
        board : Board
            current state of Rush Hour board
        boolean or None : 
            - True : indicating a solution is found
            - False : indicating no solution is found yet
            - None: : no solution is found at all
        '''
        solvable = self.board.solve()
        if solvable:
            return self.board, solvable
        moves = self.board.get_states()
        best_score = self.board.calculate_value()
        best_moves = []

        worst_score = 0
        worst_moves = []

        for move in moves:
            if move.__repr__() not in self.state_cache:
                score = move.calculate_value()
                print(f'Level {len(self.states)} node: {score}')
                
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
            best_moves = moves
        
        if len(best_moves) == 1:
            self.board = best_moves[0]
        else:
            print(best_moves)
            random_move = random.randint(0, len(best_moves) - 1)
            self.board = best_moves[random_move]

        if len(self.state_cache) >= self.max_state_cache_size:
            self.state_cache.pop()

        self.state_cache.add(self.board.repr())
        self.states.append(copy.deepcopy(self.board))
        print('Chosen board:', self.board.calculate_value(), self.board.__repr__(), self.board.get_amount_of_states())
        return self.board, False
        
        
    def get_name(self):
        return 'Greedy' #+ 'variant'