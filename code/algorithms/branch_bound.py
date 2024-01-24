from typing import Protocol
import copy
import 

class BranchAndBound(Protocol):
    def __init__(self, board):
        self.board = copy.deepcopy(board)

        self.states = [copy.deepcopy(self.board)]

        self.best_solution = None
    
    def get_next_state(self):
        return self.states.pop()

    def get_children(self):

        # receives the list of all the next possible nodes 
        childs = self.board.get_moves(True)

        for child in childs:
            new_board = copy.deepcopy(child)
            self.states.append(new_board)

    def run(self):
        pass
    def get_name(self):
        return 'Branch_bound'