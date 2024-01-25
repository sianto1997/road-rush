from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
import copy

class BreadthFirst(Algorithm):
    def __init__(self, board: Board):
        self.board = copy.deepcopy(board)
        
        self.states = [copy.deepcopy(self.board)]
        self.archive = set()
        self.visited_states = 0
    
    def get_next_state(self):
        return self.states.pop(0)

    def build_children(self):
        possible_states = self.board.get_moves(output_as_states=True)

        for state in possible_states:
            if not state.__repr__() in self.archive:
                self.states.append(state)
                self.archive.add(state.__repr__())

    def run(self):
        if not len(self.states) == 0:
            
            # get next state through dequeue
            self.board = self.get_next_state()
            self.visited_states += 1
            
            if self.board.solve():
                print(f'A solution is found, amount of states visited: {self.visited_states}.')
                return self.board, False
            
            self.build_children()
            return self.board, True
        else:
            print(f'No solution is found, amount of states visited: {self.visited_states}.')
            return self.board, False
    
    def get_name(self):
        return 'BreadthFirst'