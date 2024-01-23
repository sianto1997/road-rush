from typing import Protocol

class BreadthFirst(Protocol):
    def __init__(data, board):
        pass
    def run(self):
        pass
    def get_name(self):
        return 'BreadthFirst'