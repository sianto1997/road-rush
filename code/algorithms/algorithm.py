from typing import Protocol

class Algorithm(Protocol):
    '''
    The algorithm protocol makes sure all algorithms used in runner have at least the methods of this protocol 
    '''
    def __init__(self, board, **kwargs) -> None:
        '''
        Parameters
        ----------
        - board : Board
            the initial board
        - **kwargs : Kwargs
            these are used for algorithm specific parameters, kwargs can be left empty if not required
        '''

    def run(self) -> None:
        '''
        Run one iteration of the algorithm
        '''
    
    def get_name(self) -> None:
        '''
        Get the name of the current algorithm for saving the result to CSV.
        '''