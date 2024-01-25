from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
import copy

class BreadthFirst(Algorithm):
    def __init__(self, board: Board, archive_on=True):
        '''
        Initialize Breadthfirst algorithm with deep copy of initial board state.

        Input:
        - board = the initial state of Rush Hour board.
        '''

        self.board = copy.deepcopy(board)
        
        # using queue to store states you still need to look into
        self.states = [copy.deepcopy(self.board)]
        
        # keep track of the states which are already visited
        if archive_on:
            self.archive = set()
        
        self.visited_states = 0
    
    def get_next_state(self):
        '''
        Get
        '''
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
                return self.board, False, True
            
            self.build_children()
            return self.board, True, False
        
        else:
            print(f'No solution is found, amount of states visited: {self.visited_states}.')
            return self.board, False, False
    
    def get_name(self):
        return f'BreadthFirst_Archive{True}_VisitedStates{self.visited_states}'