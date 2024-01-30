from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
import copy

class BreadthFirst(Algorithm):
    def __init__(self, board: Board):
        '''
        Initialize Breadthfirst algorithm with deep copy of initial board state.

        Input:
        - board = the initial state of Rush Hour board.
        '''

        self.board = copy.deepcopy(board)
        
        # Using queue to store states you still need to look into
        self.states = [copy.deepcopy(self.board)]
        
        # Keep track of the states which are already visited
        self.archive = set()
        
        self.visited_states = 0
    
    def get_next_state(self):
        '''
        Get next state through a dequeue operation on the list of states.
        
        Output:
        - The next state of the board.
        '''
        return self.states.pop(0)

    def build_children(self):
        '''
        Get possible states from current board state and add to list if state is not visited before.
        '''
        
        # get possible states from current board state
        possible_states = self.board.get_states()

        for state in possible_states:

            # use representation to make algorithm faster
            if state.repr() not in self.archive:
                self.states.append(state)
                self.archive.add(state.repr())

    def run(self):
        '''
        Run the BreadthFirst algorithm until all possible states are visited.
        
        Output:
        - Final state of Rush Hour board.
        - A boolean indicating if a solution is found.
        '''
        # check if there are (still) states to explore
        if self.states != 0:
            
            # get next state through dequeue
            self.board = self.get_next_state()
            self.visited_states += 1
            
            # check if current board state is a solution
            if self.board.solve():
                print(f'A solution is found, amount of states visited: {self.visited_states}.')
                return self.board, True
            
            # get possible states for to explore further
            self.build_children()
            
            return self.board, False
        
        else:
            print(f'No solution is found, amount of states visited: {self.visited_states}.')
            return self.board, None
    
    def get_name(self):
        '''
        Get name of the algorithm to save CSV-file.
        
        Output:
        - Name of the algorithm in string.
        '''
        return f'BreadthFirst_Archive{True}_VisitedStates{self.visited_states}'