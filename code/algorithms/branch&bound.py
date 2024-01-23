from typing import Protocol
import copy

class Branch_bound(Protocol):
    def __init__(self, graph, states):
        pass
    def run(self, board):
        pass
    def get_name(self):
        return 'Branch_bound'