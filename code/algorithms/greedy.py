from enum import Enum
import random

from code.algorithms.algorithm import Algorithm

class Greedy(Algorithm):
    def __init__(self, board):
        self.board = board
        
    def run(self):
        moves = self.board.get_moves(True)
        print(len(moves))
        return self.board
        best_move = None
        best_score = -1000
        # print('ml', len(moves))
        if len(moves) >= 1:
            for move in moves:
                score = move.calculate_value()
                # print('s', score)
                if score <= best_score:
                    best_move = move
                    best_score = score
            
                    self.board = best_move
                    print(best_score)
        
        
    def get_name(self):
        return 'Greedy' + 'variant'