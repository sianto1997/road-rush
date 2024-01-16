from datetime import datetime
from code.classes.board import Board
import math
import time
import pandas as pd


class Runner:
    def __init__(self, max_moves, amount_of_experiments, input_file, output_directory, output_check50, visualize):
        """
        Initializing runner
        """
        if max_moves == 0:
            self.max_moves = math.inf
        else:
            self.max_moves = max_moves

        self.file_name = input_file.split('/')[-1]
        self.start_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.output_directory = output_directory
        self.output_check50 = output_check50
        self.amount_of_experiments = amount_of_experiments
        self.visualize = visualize


    # Deprecated
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

    def run(self, input, csv, algorithm_type, save_threshold, **kwargs):
        """
        Start random experiment

        Input:
        - input: Input filename (used for extracting board size)
        - csv: Input of file (used for initializeing cars)
        - move_method: Inputs which limitation is used for running simulations
        - save_threshold: Save result only if amount of moves is lower than this threshold
        """
        # print(move_method, MoveMethods.RandomAll, MoveMethods(move_method) == MoveMethods.RandomAll)
        moves = []
        for i in range(self.amount_of_experiments):
            # Creates a object of the class Board 
            self.board = Board(input, csv, self.visualize)
            
            self.board.draw() 
            
            algorithm = algorithm_type(**kwargs)
            solved = False
        
            while not solved and self.board.get_amount_of_moves() < self.max_moves:
                if self.board.solve():
                    solved = True
                else:
                    algorithm.run(self.board)
                    
                    

            self.board.close_visualization()

            # time.sleep(10)
            
            # print(moves)

            amount_of_moves = self.board.get_amount_of_moves()
            if solved:
                moves.append(amount_of_moves)

            # Applying save_threshold to not save long (bad) solutions
            if amount_of_moves <= save_threshold and solved:
                # Save location for check 50
                if self.output_check50:
                    self.board.save_moves(f'output.csv')
                # Save in readable format
                else:
                    self.board.save_moves(f'{self.output_directory}/{self.file_name}_{algorithm.get_name()}_{solved}_{amount_of_moves}_{self.start_time}.csv')

        # Print the top solutions for comparison to other experiments 
        print(sorted(moves)[:5])

        # print(f'Average amount of moves neccesary to solve  {sum(moves) / len(moves)}')

        
        df = pd.DataFrame(moves, columns=['move']) 
        df.to_csv('random_experiments', index=False)
        # TODO: Print solve rate 
        # TODO: Print solve rate below threshold
