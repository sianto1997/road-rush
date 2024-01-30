import math
import pandas as pd
import pickle
import copy
import os
import pandas as pd
from datetime import datetime

from code.classes.board import Board
from code.classes.board_visualization import BoardVisualization

class Runner:
    def __init__(self, max_moves, amount_of_experiments, input_file, output_directory, output_check50, visualize, draw_interval, algorithm_type, save_threshold, **kwargs):
        '''
        Initializing runner

        Attributes
        ----------
        max_moves : int
            Cut-off at an amount of moves (after this the runner stops and starts next experiment if applicable)
        amount_of_experiments : int 
            The amount of experiments that the experiment runs at the maximum (after which it stops and saves the last result).
        input_file : str 
            The path of the input file (example: data/Rushhour6x6_1.csv)
        output_directory : str
            The directory to save the output to
        output_check50 : bool
            Save output as output.csv (used for check50 validation of file)
        visualize : bool 
            Whether to visualize the running experiment (using board_visualize)
        algorithm_type : Algorithm
            The algorithm to be used by the runner (needs to be of type Algorithm)
        save_threshold : int
            Save the output (csv) when the amount of moves is at or lower than this number
        **kwargs : 
            Algorithm-specific keyword arguments
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
        self.draw_interval = draw_interval
        self.i = 0
        self.input_file = input_file
        
        self.csv = pd.read_csv(input_file) 
        self.algorithm_type = algorithm_type
        self.save_threshold = save_threshold
        self.kwargs = kwargs
        self.pickle_location = f'../{self.file_name}.pickle'

    def run(self):
        '''
        Start experiment defined by init
        '''
        
        if self.visualize:
            self.visualization = BoardVisualization(self.draw_interval)

        moves = []

        while self.i < self.amount_of_experiments:
            # Using try -> catch to save on manual stop of the experiment.
            try:
                # Creates a object of the class Board 
                self.board = Board(self.input_file, self.csv)
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
                    self.visualization.draw(100000)
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
                    else:
                        # Save in readable format
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
        Saving the current experiment of pickle. This saves the current state of Runner and the objects within the current instance. Called during an experiment
        '''
        backup = copy.deepcopy(self)
        with open(self.pickle_location, 'wb') as pickle_file:
            pickle.dump(backup, pickle_file)

    def clean_object(self):
        '''
        Removing pickle of the experiment. Called at the end of the experiment
        '''
        if os.path.exists(self.pickle_location):
            os.remove(self.pickle_location) 