from typing import Protocol


class Algorithm(Protocol):
    def __init__(self, **kwargs) -> None:
        """Kwargs are used for algorithm specific parameters, kwargs can be left empty if not required"""

    def run(self, board) -> None:
        """Run the algorithm"""
    
    def get_name(self) -> None:
        """Get a name for saving the result to CSV."""