from typing import Protocol
import copy

class BranchAndBound(Protocol):
    def __init__(self, board):
        self.board = copy.deepcopy(board)

        self.states = [copy.deepcopy(self.board)]
    
    def get_next_state(self):
        return self.states.pop()

    def get_children(self):
        child = self.board.get_moves(True)

        


    def run(self):
        pass
    def get_name(self):
        return 'Branch_bound'