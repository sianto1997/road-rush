import argparse
import pandas as pd
from board import Board
from experiment import Experiment
import time

def main(input_file):

    # reads the csv and turns it into a dataframe
    csv = pd.read_csv(input_file) 

    # creates a object of the class Board 
    board = Board(input_file, True)
    board.add_cars(csv) 
    
    board.draw() 

    experiment = Experiment(board, 1000, input_file)
    experiment.start_random_experiment()

    time.sleep(12)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "reads in csv file")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input)
