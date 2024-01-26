from enum import Enum
import random

from code.algorithms.algorithm import Algorithm

class Greedy(Algorithm):
    def __init__(self, board):
        self.board = board
        self.best_move = self.board
        self.best_score = self.board.calculate_value()
        print(f'Start score = {self.best_score}')
        
    def run(self):
        moves = self.board.get_moves(True)
        print('amount_of_moves', len(moves))
        # return self.board, True
        best_move = None
        best_score = -1000
        # print('ml', len(moves))
        if len(moves) >= 1:
            for move in moves:
                score = move.calculate_value()
                print('s', score)
                if score <= best_score:
                    best_move = move
                    best_score = score
            
                    self.board = best_move
                    # print(best_score)
        if best_move == None:
            return self.board, True
        
        return best_move, False
        
        
    def get_name(self):
        return 'Greedy' + 'variant'