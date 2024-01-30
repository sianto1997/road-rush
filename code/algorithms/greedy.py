from enum import Enum
import random
import math
import copy

from code.algorithms.algorithm import Algorithm

class Greedy(Algorithm):
    def __init__(self, board, max_state_cache_size=10000):
        '''
        This is the greedy algorithm, written by Simon Antonides. It bases itself on version 2 of the Technical Description.
        
        '''
        self.board = board
        self.best_move = self.board
        self.best_score = self.board.calculate_value()
        # The state cache is created to avoid ending in an infinite loop with the same states
        self.max_state_cache_size = max_state_cache_size
        self.archive = set(self.board.__repr__())
        self.state_cache = list(self.board.__repr__())
        self.states = [copy.deepcopy(self.board)]

        print(f'Start score = {self.best_score} {self.board.__repr__()}')
        
    def run(self):
        solvable = self.board.solve()
        if solvable:
            return self.board, solvable
        moves = self.board.get_states()
        # print('amount_of_moves', len(moves))
        # return self.board, True
        best_score = 0 # self.board.calculate_value()
        best_moves = []

        worst_score = 0
        worst_moves = []

        # print('bs', best_score)
        # if len(moves) >= 1:
        for move in moves:
            # print(move.collision_map)
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
        
        # print(best_moves)
        if len(self.states) == 0 or (len(best_moves) == 0 and len(worst_moves) == 0):
            return self.board, False
            
        elif len(best_moves) == 0 and len(worst_moves) != 0:
            print(best_moves)
            print(worst_moves)
            best_moves = worst_moves
            print('hi')
            # self.board = self.states.pop()
            # return self.board, False
        
        if len(best_moves) == 1:
            self.board = best_moves[0]
        else:
            print(best_moves)
            random_move = random.randint(0, len(best_moves) - 1)
            self.board = best_moves[random_move]
            # print('SM', self.board.calculate_value())

        if len(self.state_cache) >= self.max_state_cache_size:
            self.state_cache.pop()

        self.state_cache.append(self.board.__repr__())
        self.states.append(copy.deepcopy(self.board))
        print('Chosen board:', self.board.calculate_value(), self.board.__repr__(), self.board.get_amount_of_states())
        return self.board, False
        
        
    def get_name(self):
        return 'Greedy' #+ 'variant'