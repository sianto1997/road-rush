import math
from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
import copy

from code.classes.score import Score

class GreedyDepthFirst(Algorithm):
    '''
    The Greedy DepthFirst algorithm is a variant of the Greedy Algorithm. It uses Depth First based on the board scoring

    Attributes
    ----------
    board : Board
        The current state of the Rush Hour board
    best_state : Board
        The best state until now
    best_score : int
        The score of the best state until now
    states : list of Board
        A stack to store states you still need to look into
    archive : set of int
        Keeps track of the states which are already visited
    visited_states : int
        Amount of states the algorithm did look at to find a solution
    '''
    def __init__(self, board: Board):
        '''
        Parameters
        ----------
        board : Board
            The initial state of the board.
        '''
        self.score = Score()

        self.board = copy.deepcopy(board)
        
        self.best_state = self.board
        self.best_score = - math.inf
        self.worst_score = math.inf
        
        self.states = [copy.deepcopy(self.board)]

        self.archive = set()
        self.archive.add(self.board.__repr__())

        self.state_cache = []
        self.state_cache_limit = 3
        
        self.visited_states = 0
    
    def get_next_state(self):
        '''
        Get next state through a unstack operation on the list of states
        
        Output
        ------
        board : Board
            The next or current state of the board
        '''
        new_state = self.states.pop()
        if new_state not in self.state_cache:
            self.state_cache.append(new_state)
            if len(self.state_cache) > self.state_cache_limit:
                self.state_cache.pop()
        else:
            new_state = self.board

        return new_state

    def possible_states(self):
        '''
        Get possible states from current board state and add to stack if state is not visited before
        '''
        score_boundary = self.best_score - 128

        # Check if board is as good as best score of the current depth
        if self.score.calculate_value(self.board) >= score_boundary:
            possible_states = self.board.get_states()

            for state in possible_states:
                # Use representation to make algorithm faster
                if state.__repr__() not in self.archive:
                    self.states.append(state)
                    self.archive.add(state.__repr__())

    def run(self):
        '''
        Run one iteration of the Greedy DepthFirst algorithm
        
        Output
        ------
        board : Board
            Current state of Rush Hour board
        solved : bool or None 
            - True : indicating a solution is found
            - False : indicating no solution is found yet
            - None: : no solution is found at all
        '''
        # Check if there are (still) states to explore
        if len(self.states) == 0:
            print(f'No solution is found, amount of states visited: {self.visited_states}.')
            return self.board, None
        else:
            
            # Get next state through dequeue
            self.board = self.get_next_state()
            board_score = self.score.calculate_value(self.board)
            self.visited_states += 1

            if board_score > self.best_score:
                self.best_score = board_score
                self.best_state = copy.deepcopy(self.board)

            if board_score < self.worst_score:
                self.worst_score = board_score

            self.visited_states += 1
            
            if self.board.solve():
                print(f'A solution is found, amount of states visited: {self.visited_states}.')
                return self.board, True
            
            # Get possible states for to explore further
            self.possible_states()
            
            return self.board, False
    
    def get_name(self):
        '''
        Get name of the algorithm to save CSV-file
        
        Output
        ------
        name : str
            Name of the algorithm
        '''
        return f'GreedyDepthFirst_VisitedStates{self.visited_states}'