import copy
from code.algorithms.algorithm import Algorithm
from code.classes.board import Board

class BranchAndBound(Algorithm):
    '''
    A Dept first algoritem that does not search on a deeper level than the first found solution.
    '''
    
    def __init__(self, board: Board):
        self.board = copy.deepcopy(board)

        self.states = [copy.deepcopy(self.board)]

        self.best_solution = None
        self.archive = set()
        
        self.visited_states = 0
    
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
            if child not in self.archive: 
                self.states.append(child)
                self.archive.add(child.__repr__())

    def run(self):
        '''
        Runs the algorithm until the best possible solution is found 
        '''
        if self.states:
            print(len(self.states))
            self.board = self.get_next_state()
            self.visited_states += 1 
            if self.board.solve():
                print("A solution is found!")
                return self.board, True
            
            self.get_children()

        return self.board, False 
        

    def get_name(self):
        '''
        Returns the name of the algorithm
        '''
        return 'BranchAndBound'