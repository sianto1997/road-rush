from code.algorithms.algorithm import Algorithm
from queue import Queue
import copy

class BreadthFirst(Algorithm):
    def __init__(self, board):
        self.board = copy.deepcopy(board)
        
        # create queue to store states FIFO
        # self.states = Queue()
        self.states = [copy.deepcopy(self.board)]
        self.archive = set()
    
    def get_next_state(self):
        return self.states.pop(0)

    def build_children(self):
        possible_states = self.board.get_moves(True)

        for state in possible_states:
            if not state.__repr__() in self.archive:
                self.states.append(state)
                self.archive.add(state.__repr__())

    def run(self):
        if not len(self.states) == 0:
            
            # get next state through dequeue
            self.board = self.get_next_state()
            print(self.board)
            if self.board.solve():
                print('A solution is found!')
                # return self.board
                return True
            
            self.build_children()
            print(len(self.states))
        else:
            # print('No solution is found.')
            return False
    
    def get_name(self):
        return 'BreadthFirst'