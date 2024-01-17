from typing import Protocol

class BreadthFirst(Protocol):
    def __init__(data):
        pass
    def run(self, board):
        pass
    def get_name(self):
        return 'BreadthFirst'