from typing import Protocol

class Genetic(Protocol):
    def __init__(data):
        pass
    def run(self, board):
        pass
    def get_name(self):
        return 'Genetic'