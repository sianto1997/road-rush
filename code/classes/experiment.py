import random
from datetime import datetime

class Experiment:
    def __init__(self, board, move_tries, input_file):
        self.board = board
        self.move_tries = move_tries
        self.file_name = input_file.split('/')[-1]
        self.start_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        print(self.file_name)



    def simple_experiment(self):
        # self.try_move(self.cars[0], -1)
        
        # self.try_move(self.cars[1], -1)

        # self.try_move(self.cars[2], 1)

        self.move(self.cars[-4], -1)
        self.move(self.cars[-5], 2)
        self.move(self.cars[-5], -1)
        self.move(self.cars[-5], 2)

    def start_random_experiment(self):
        solved = False
        for _ in range(self.move_tries):
            
            car_index = random.randint(0, len(self.board.cars) - 1)
            # print(len(self.cars), car_index)
            self.board.move(self.board.cars[car_index], random.randint(-self.board.size,self.board.size))
            if self.board.finish():
                solved = True
                break

        self.board.save_moves(self, f'data/{self.file_name}_{self.start_time}_{solved}.csv')