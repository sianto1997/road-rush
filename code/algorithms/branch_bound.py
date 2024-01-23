from typing import Protocol
import copy

class BranchAndBound(Protocol):
    def __init__(self, board, graph, states):
        pass
    def run(self):
        pass
    def get_name(self):
        return 'Branch_bound'