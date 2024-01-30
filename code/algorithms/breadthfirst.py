from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
import copy

class BreadthFirst(Algorithm):
    '''
    Initialize Breadthfirst algorithm with deep copy of initial board state

    Attributes
    ----------
    board : obj
        the initial state of a Rush Hour board
    states : list
        a queue to store states you still need to look into
    archive : set
        keeps track of the states which are already visited
    visited_states : int
        amount of states the algorithm did look at to find a solution
    '''

    def __init__(self, board: Board):
        '''
        Parameters
        ----------
        board : obj
            the initial state of a Rush Hour board
        '''
        self.board = copy.deepcopy(board)
        
        self.states = [copy.deepcopy(self.board)]
        
        self.archive = set()
        
        self.visited_states = 0
    
    def get_next_state(self):
        '''
        Get next state through a dequeue operation on the list of states
        
        Output
        ------
        board : obj
            the next state of the board
        '''
        return self.states.pop(0)

    def possible_states(self):
        '''
        Get possible states from current board state and add to list if state is not visited before
        '''
        
        possible_states = self.board.get_states()

        for state in possible_states:

            if state.__repr__() not in self.archive:
                self.states.append(state)
                self.archive.add(state.repr())

    def run(self):
        '''
        Run the BreadthFirst algorithm until all possible states are visited
        
        Output
        ------
        board : obj
            final state of Rush Hour board
        boolean or None : 
            - True : indicating a solution is found
            - False : indicating no solution is found yet
            - None: : no solution is found at all
        '''
        if self.states == 0:
            print(f'No solution is found, amount of states visited: {self.visited_states}.')
            return self.board, None
        
        self.board = self.get_next_state()
        self.visited_states += 1
        
        if self.board.solve():
            print(f'A solution is found, amount of states visited: {self.visited_states}.')
            return self.board, True
        
        self.possible_states()
        
        return self.board, False
        
    def get_name(self):
        '''
        Get name of the algorithm to save CSV-file
        
        Output
        ------
        str : name of the algorithm
        '''
        return f'BreadthFirst_Archive{True}_VisitedStates{self.visited_states}'