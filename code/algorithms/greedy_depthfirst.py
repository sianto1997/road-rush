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
    level_score : int
        The average score of a the current level
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
        self.best_score = [- math.inf]
        self.level_score = [- math.inf]
        
        self.states = [copy.deepcopy(self.board)]

        self.archive = set()
        self.archive.add(self.board.__repr__())
        
        self.visited_states = 0
    
    def get_next_state(self):
        '''
        Get next state through a unstack operation on the list of states
        
        Output
        ------
        board : Board
            The next state of the board
        '''
        new_state = self.states.pop()
        if len(new_state.archive) > len(self.best_score):
            self.best_score.append(- math.inf)

        return new_state

    def possible_states(self):
        '''
        Get possible states from current board state and add to stack if state is not visited before
        '''
        # Check if board is as good as best score of the current depth
        if self.score.calculate_value(self.board) == self.best_score[len(self.board.archive) - 1]:
            possible_states = self.board.get_states()
            scores = []
            archive = set()
            states = []

            for state in possible_states:
                # Use representation to make algorithm faster
                if state.repr() not in self.archive:
                    states.append(state)
                    archive.add(state.repr())
                    scores.append(self.score.calculate_value(state))

            score = - math.inf

            if len(scores) > 0:
                score = sum(scores) / len(scores)

            if len(self.board.archive) < 100 or score >= self.level_score[len(self.level_score) - 1] * 0.75:
                self.level_score.append(score)

                self.states.extend(states)
                self.archive.update(archive)

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
            
            # Bet next state through dequeue
            self.board = self.get_next_state()
            board_score = self.score.calculate_value(self.board)
            self.visited_states += 1

            if board_score >= self.best_score[len(self.board.archive) - 1] or board_score >= self.level_score[len(self.board.archive) - 1]: #(sum(self.best_score) / len(self.best_score)) * 5:
                self.best_score[len(self.board.archive) -1] = board_score
                self.best_state = copy.deepcopy(self.board)

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