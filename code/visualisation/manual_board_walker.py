from code.algorithms.algorithm import Algorithm
from code.classes.board import Board
from code.classes.score import Score

class ManualBoardWalker(Algorithm):
    '''
    This class is being used to walk on a board manually
    '''
    def __init__(self, board : Board):
        self.board = board
        self.score = Score()
        self.i = 0
        self.cars = [
            # board.get_car_by_index(4),
            # board.get_car_by_index(0),
            # board.get_car_by_index(2)
            ]
        self.moves = [
            -3,
            1,
            2
            ]
        
        self.moves2 = self.board.get_states()
        print(f'start {self.score.calculate_value(self.board)}')

    def run(self):
        print(f'run {self.score.calculate_value(self.board)}')
        if self.i < len(self.cars):
            car = self.cars[self.i]
            move = self.moves[self.i]
            # print(car, move)
            print(self.board.move(car, move))

            self.i += 1
            return self.board, False
        elif self.i < len(self.moves2):
            # print(car, move)
            # print(self.board.move(car, move))
            self.board = self.moves2.pop()
            self.i += 1
            return self.board, False
        else:
            # Quit
            return self.board, None

    def get_name(self):
        return 'ManualBoardWalker'