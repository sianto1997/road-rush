from enum import Enum
import random

class Greedy(Algorithm):
    def __init__(self, board):
        self.board = board
        
    def run(self):
        pass
        
    def get_name(self):
        return 'Greedy' + 'variant'