from typing import Protocol

class HillClimber(Protocol):
    def __init__(data, board):
        pass
    def run(self):
        pass
    def get_name(self):
        return 'HillClimber'