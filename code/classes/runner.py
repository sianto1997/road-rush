from datetime import datetime
from code.classes.board import Board
import math
import time
import pandas as pd
import pickle
import copy

class Runner:
    def __init__(self, max_moves, amount_of_experiments, input_file, output_directory, output_check50, visualize, input, csv, algorithm_type, save_threshold, **kwargs):
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
        self.i = 0
        self.input = input
        self.csv = csv
        self.algorithm_type = algorithm_type
        self.save_threshold = save_threshold
        self.kwargs = kwargs


    def run(self):
        """
        Start random experiment

        Input:
        - input: Input filename (used for extracting board size)
        - csv: Input of file (used for initializeing cars)
        - move_method: Inputs which limitation is used for running simulations
        - save_threshold: Save result only if amount of moves is lower than this threshold
        """
        moves = []
        while self.i < self.amount_of_experiments:
            # Creates a object of the class Board 
            try:
                # print(self.i)
                self.board = Board(self.input, self.csv, self.visualize)
                
                algorithm = self.algorithm_type(self.board, **self.kwargs)
                solved = False
                no_quit = True

                while (not solved and self.board.get_amount_of_moves() < self.max_moves) and no_quit:
                    if self.board.solve():
                        solved = True
                    else:
                        (self.board, no_quit) = algorithm.run()
                self.i += 1

                # time.sleep(10)
                self.board.pause(100000)

                self.board.close_visualization()

                amount_of_moves = self.board.get_amount_of_moves()
                print(amount_of_moves)
                if solved:
                    moves.append(amount_of_moves)

                # Applying save_threshold to not save long (bad) solutions
                if (self.save_threshold == 0 or amount_of_moves <= self.save_threshold) and solved:
                    # Save location for check 50
                    if self.output_check50:
                        self.board.save_moves(f'output.csv')
                    # Save in readable format
                    else:
                        self.board.save_moves(f'{self.output_directory}/{self.file_name}_{algorithm.get_name()}_{solved}_M{amount_of_moves}_S{self.board.get_amount_of_states()}_{self.start_time}.csv')
            except (KeyboardInterrupt, SystemExit):
                # Save when quitting
                self.save_object()
                exit()

            # Save each iteration while running
            self.save_object()


        # Print the top solutions for comparison to other experiments 
        print(sorted(moves)[:5])

        # print(f'Average amount of moves neccesary to solve  {sum(moves) / len(moves)}')

        
        df = pd.DataFrame(moves, columns=['move']) 
        df.to_csv('random_experiments.csv', index=False)
        # TODO: Print solve rate 
        # TODO: Print solve rate below threshold
    def save_object(self):
        backup = copy.deepcopy(self) #(in ons geval runner instance)
        with open('output/runner.pickle', 'wb') as pickle_file:
            pickle.dump(backup, pickle_file)