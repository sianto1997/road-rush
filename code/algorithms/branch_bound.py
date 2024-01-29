import copy
from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
from collections import defaultdict
class BranchAndBound(Algorithm):
    '''
    A depth first algorithm that does not search on a deeper level than the first found solution.
    '''
    
    def __init__(self, board: Board):
        self.board = copy.deepcopy(board)

        self.states = [copy.deepcopy(self.board)]

        self.best_solution = None
        self.archive = defaultdict(lambda: float('inf'))
        
        self.visited_states = 0
        self.depth = float('inf')

    def get_next_state(self):
        '''
        Gets the next state out of the list. 
        '''
        return self.states.pop()

    def get_children(self):
        '''
        Creates the children nodes for the list 
        '''

        # receives a list of all the next possible nodes 
        childs = self.board.get_moves(output_as_states=True)
        
        for child in childs:
            # print('doei')
            if self.archive[child.__repr__()] > len(child.moves) and len(child.moves) < self.depth: 
            # if child.__repr__() not in self.archive and len(child.moves) < self.depth: 
                # print('hoi')
                self.states.append(child)
                self.archive[child.__repr__()] = len(child.moves)

    def run(self):
        '''
        Runs the algorithm until the best possible solution is found 
        '''
        if self.states:
            self.board = self.get_next_state()
            self.visited_states += 1 
            if self.board.solve():
                print(f"A solution is found! Amount of moves visited: {len(self.board.moves)}")
                self.depth = len(self.board.moves)
                self.best_solution = copy.deepcopy(self.board)

        elif not self.states and self.best_solution is not None:
            print(f"A solution is found! Amount of states visited: {self.visited_states}")
            return self.best_solution, True

        self.get_children()
        

        return self.board, False 
        

    def get_name(self):
        '''
        Returns the name of the algorithm
        '''
        return 'BranchAndBound'