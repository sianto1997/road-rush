from typing import Protocol

class Bruteforce(Protocol):
    def __init__(data):
        pass
    def run(self, board):
        pass
    def get_name(self):
        return 'Bruteforce'