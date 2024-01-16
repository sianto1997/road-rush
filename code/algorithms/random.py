from enum import Enum
from code.algorithms.algorithm import Algorithm
import random

class MoveMethods(Enum):
    """
    The MoveMethods determine how far a car can move in one move.
    RandomAll can move between and including - board_size to and including board_size
    RandomOne can move -1 or +1
    RandomTwo can move between and including -2 or +2
    RandomThree can move between and including -3 or +3
    """
    RandomAll = 0
    RandomOne = 1
    RandomTwo = 2
    RandomThree = 3

class Random(Algorithm):
    def __init__(self, move_method = MoveMethods.RandomAll):
        self.move_method = move_method
        print(self.get_name())
            

    def run(self, board):
        self.board = board
        car_index = random.randint(0, len(self.board.cars) - 1)

        if MoveMethods(self.move_method) == MoveMethods.RandomAll:
            steps = random.randint(-self.board.size,self.board.size)
        else:
            steps = random.randint(-self.move_method,self.move_method)

        self.board.move(self.board.cars[car_index], steps)

    def get_name(self):
        return MoveMethods(self.move_method).name