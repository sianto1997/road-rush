import random

class Experiment:
    def __init__(self, board):
        self.board = board


    def simple_experiment(self):
        # self.try_move(self.cars[0], -1)
        
        # self.try_move(self.cars[1], -1)

        # self.try_move(self.cars[2], 1)

        self.try_move(self.cars[-4], -1)
        self.try_move(self.cars[-5], 2)
        self.try_move(self.cars[-5], -1)
        self.try_move(self.cars[-5], 2)

    def start_random_experiment(self):
        for _ in range(1000):
            
            car_index = random.randint(0, len(self.cars) - 1)
            # print(len(self.cars), car_index)
            self.board.try_move(self.cars[car_index], random.randint(-6,6))


        self.board.save_moves(self, 'data/1.csv')