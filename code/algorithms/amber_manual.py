from typing import Protocol
import time

class AmberManual(Protocol):
    def __init__(self, board):
        self.board = board
        self.i = 0
        self.cars = [
            board.cars[4],
            board.cars[0],
            board.cars[2]
            ]
        self.moves = [
            -3,
            1,
            2
            ]

    def run(self):
        # print(f'run {self.i}')
        if self.i < len(self.cars):
            car = self.cars[self.i]
            move = self.moves[self.i]
            self.board.pause(50000)
            print(self.board.move(car, move))

            self.i += 1
            return False
        else:
            # Quit
            return True

    def get_name(self):
        return 'AmberManual'