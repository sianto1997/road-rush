import random
from datetime import datetime
from board import Board
from enum import Enum
import time

class MoveMethods(Enum):
    RandomMax = 0
    RandomOne = 1
    RandomTwo = 2

class Experiment:
    def __init__(self, max_moves, amount_of_experiments, input_file, output_directory, output_check50, visualize):
        """
        Initializing experiment
        """
        self.max_moves = max_moves
        self.file_name = input_file.split('/')[-1]
        self.start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # print(self.file_name)
        self.output_directory = output_directory
        self.output_check50 = output_check50
        self.amount_of_experiments = amount_of_experiments
        self.visualize = visualize



    def simple_experiment(self):
        """
        Simple manual experiment
        """
        self.move(self.cars[0], -1)
        
        self.move(self.cars[1], -1)

        self.move(self.cars[2], 1)

        self.move(self.cars[-4], -1)
        self.move(self.cars[-5], 2)
        self.move(self.cars[-5], -1)
        self.move(self.cars[-5], 2)

    def start_random_experiment(self, input, csv, move_method, save_threshold):
        """
        Start random experiment

        Input:
        - move_method: Inputs which limitation is used for running simulations.
        """
        moves = set()
        for i in range(self.amount_of_experiments):
            # creates a object of the class Board 
            self.board = Board(input, csv, self.visualize)
            
            self.board.draw() 
            
            # time.sleep(100)

            solved = False
            while solved or self.board.get_amount_of_moves() < self.max_moves:
                car_index = random.randint(0, len(self.board.cars) - 1)

                if move_method == MoveMethods.RandomMax:
                    steps = random.randint(-self.board.size,self.board.size)
                else:
                    steps = random.randint(-move_method,move_method)
                
                self.board.move(self.board.cars[car_index], steps)
                if self.board.finish():
                    print('x')
                    solved = True

            amount_of_moves = self.board.get_amount_of_moves()
            moves.add(amount_of_moves)

            # Applying save_threshold to not save long (bad) solutions
            if amount_of_moves <= save_threshold:
                # Save location for check 50
                if self.output_check50:
                    self.board.save_moves(f'output.csv')
                # Save in readable format
                else:
                    self.board.save_moves(f'{self.output_directory}/{self.file_name}_{MoveMethods(move_method).name}_{solved}_{amount_of_moves}_{self.start_time}.csv')

        # Print the top solutions for comparison to other experiments 
        print(moves)