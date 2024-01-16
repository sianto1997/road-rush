from enum import Enum
import random

class MoveMethods(Enum):
    RandomAll = 0
    RandomOne = 1
    RandomTwo = 2

class Random():
    def __init__(self, board):
        self.board = board

    def run(self, move_method = MoveMethods.RandomAll):
        car_index = random.randint(0, len(self.board.cars) - 1)

        if MoveMethods(move_method) == MoveMethods.RandomAll:
            steps = random.randint(-self.board.size,self.board.size)
        else:
            steps = random.randint(-move_method,move_method)

        self.board.move(self.board.cars[car_index], steps)