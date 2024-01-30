import copy
from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
from collections import defaultdict

class BranchAndBound(Algorithm):
    '''
    A depth first algorithm that does not search deeper than the previously found solution

    Attributes
    ----------

    board : obj
        A state of the Board class 
    states : list
        a stack storing the states that need to be used next by the algorithm
    best_solution : NoneType
        A variable to store the best found solution
    archive : dict
        stores the states that have already been visited
    visited_state : int
        keeps track of all the states that have been visited 
    depth: int
        Keeps track of how deep the solution is found 
    '''
    
    def __init__(self, board: Board):
        self.board = copy.deepcopy(board)

        self.states = [copy.deepcopy(self.board)]

        self.best_solution = None

        # Taking the maximum depth as te optimal solution of Random
        self.archive = defaultdict(lambda: 538)# float('inf'))
        
        self.visited_states = 0
        self.depth = float('inf')

    def get_next_state(self):
        '''
        Gets the next state out of the stack

        Output
        ------
        obj: a Board
        '''
        return self.states.pop()

    def get_children(self):
        '''
        Creates the children nodes for the list 
        '''

        # A list with al the possible next states 
        children = self.board.get_states()
        
        for child in children:

            # checks if child is lower than the one already stored in the archive and 
            # if the amount of moves is lower than the current depth
            if self.archive[child.__repr__()] > len(child.moves) and len(child.moves) < self.depth:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
                self.states.append(child)
                self.archive[child.__repr__()] = len(child.moves)

    def run(self):
        '''
        Runs the algorithm until the best possible solution is found 

        output
        ------
        best_solution : obj
            the best found board at the moment a solution is found 
        board : obj

        boolean : 
            - True: solution is found 
            _ False: solution is not found 
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

        output
        ------
        str : 
            Name of the used algoritm
        '''
        return 'BranchAndBound'