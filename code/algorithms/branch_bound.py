import copy

from code.classes.board import Board


class BranchAndBound(Algorithm):
    def __init__(self, board: Board):
        self.board = copy.deepcopy(board)

        self.states = [copy.deepcopy(self.board)]

        self.best_solution = None
    
    def get_next_state(self):
        return self.states.pop()

    def get_children(self):

        # receives the list of all the next possible nodes 
        childs = self.board.get_moves(output_as_states=True)

        for child in childs:
            self.states.append(child)

    def run(self):
        pass
    def get_name(self):
        return 'Branch_bound'