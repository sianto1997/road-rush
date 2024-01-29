from datetime import datetime
from code.classes.board import Board
from code.classes.board_visualization import BoardVisualization
import math
import time
import pandas as pd
import pickle
import copy
import os

class Runner:
    def __init__(self, max_moves, amount_of_experiments, input_file, output_directory, output_check50, visualize, algorithm_type, save_threshold, **kwargs):
        '''
        Initializing runner

        Input:
        - max_moves (int): Max move
        - amount_of_experiments (int): The amount of experiments that the experiment runs at the maximum (after which it stops and saves the last result).
        - input_file
        - output_directory
        - output_check50 (bool)
        - visualize (bool)
        - input
        - csv
        - algorithm_type (Algorithm)
        - save_threshold (int)
        - **kwargs: Algorithm-specific keyword arguments

        
        '''
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
        
        # reads the csv and turns it into a dataframe
        self.csv = pd.read_csv(input) 
        self.algorithm_type = algorithm_type
        self.save_threshold = save_threshold
        self.kwargs = kwargs
        self.pickle_location = f'../{input_file}.pickle'


    def run(self):
        """
        Start random experiment

        Input:
        - input: Input filename (used for extracting board size)
        - csv: Input of file (used for initializeing cars)
        - move_method: Inputs which limitation is used for running simulations
        - save_threshold: Save result only if amount of moves is lower than this threshold
        """
        
        if self.visualize:
            self.visualization = BoardVisualization()
        moves = []
        while self.i < self.amount_of_experiments:
            # Creates a object of the class Board 
            try:
                # print(self.i)
                self.board = Board(self.input, self.csv)
                if self.visualize:
                    self.visualization.replace(self.board)

                
                algorithm = self.algorithm_type(self.board, **self.kwargs)
                solved = False

                while (not solved and self.board.get_amount_of_moves() < self.max_moves) and solved != None:

                    (self.board, solved) = algorithm.run()
                        
                    if self.visualize:
                        self.visualization.replace(self.board)
                        self.visualization.draw()
                        
                self.i += 1

                if self.visualize:
                    self.visualization.pause(100000)
                    self.visualization.close()


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

        df = pd.DataFrame(moves, columns=['move']) 
        df.to_csv(f'{self.file_name}_{algorithm.get_name()}_random_experiments_S{self.start_time}_E{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.csv', index=False)

        self.clean_object()


    def save_object(self):
        '''
        Saving the current experiment of pickle. This saves the current state of Runner and the objects within the current instance. Called during an experiment.
        '''
        backup = copy.deepcopy(self)
        with open(self.pickle_location, 'wb') as pickle_file:
            pickle.dump(backup, pickle_file)

    def clean_object(self):
        '''
        Removing pickle of the experiment. Called at the end of the experiment.
        '''
        os.remove(self.pickle_location) 
        
        self.clean_object()
