from code.algorithms.algorithm import Algorithm
from code.classes.board import Board

class ManualBoardWalker(Algorithm):
    def __init__(self, board : Board):
        self.board = board
        self.i = 0
        self.cars = [
            board.get_car_by_id(4),
            board.get_car_by_id(0),
            board.get_car_by_id(2)
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
            self.board.pause(10)
            print(self.board.move(car, move))

            self.i += 1
            return False
        else:
            # Quit
            return True

    def get_name(self):
        return 'ManualBoardWalker'