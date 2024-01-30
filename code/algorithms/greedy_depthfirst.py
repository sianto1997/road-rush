import math
from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
import copy

class GreedyDepthFirst(Algorithm):
    '''
    Initialize Greedy DepthFirst algorithm with deep copy of initial board state.

    Input:
    - board (Board): The initial state of Rush Hour board.
    '''
    def __init__(self, board: Board):

        self.board = copy.deepcopy(board)
        
        self.states = [copy.deepcopy(self.board)]
        
        self.archive = set()
        self.archive.add(self.board.repr())
        
        self.visited_states = 0
        self.best_state = self.board
        self.best_score = [- math.inf]
        self.level_score = [- math.inf]
    
    def get_next_state(self):
        '''
        Get next state through a destack operation on the list of states.
        
        Output:
        - The next state of the board.
        '''
        new_state = self.states.pop()
        if len(new_state.archive) > len(self.best_score):
            self.best_score.append(- math.inf)

        return new_state

    def build_children(self):
        '''
        Get possible states from current board state and add to list if state is not visited before.
        '''
        # len(self.archive) < 200 or 
        if self.board.calculate_value() == self.best_score[len(self.board.archive) - 1]:
            # get possible states from current board state
            possible_states = self.board.get_states()
            scores = []
            archive = set()
            states = []
            for state in possible_states:

                # Use representation to make algorithm faster
                if state.repr() not in self.archive:
                    states.append(state)
                    archive.add(state.repr())
                    scores.append(state.calculate_value())
            score = - math.inf
            if len(scores) > 0:
                score = sum(scores) / len(scores)

            if len(self.board.archive) < 100 or score >= self.level_score[len(self.level_score) - 1] * 0.75:
                self.level_score.append(score)

                self.states.extend(states)
                self.archive.update(archive)

    def run(self):
        '''
        Run the Greedy DepthFirst algorithm until all possible states are visited.
        
        Output:
        - Final state of Rush Hour board.
        - A boolean indicating if a solution is found.
        '''
        # check if there are (still) states to explore
        if len(self.states) != 0:
            
            # get next state through dequeue
            self.board = self.get_next_state()
            board_score = self.board.calculate_value()
            if board_score >= self.best_score[len(self.board.archive) - 1] or board_score >= self.level_score[len(self.board.archive) - 1]: #(sum(self.best_score) / len(self.best_score)) * 5:
                self.best_score[len(self.board.archive) -1] = board_score
                self.best_state = copy.deepcopy(self.board)
                # print(self.best_score[len(self.board.archive) - 1])

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
        return f'GreedyDepthFirst_VisitedStates{self.visited_states}'