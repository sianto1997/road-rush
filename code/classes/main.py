import argparse
import pandas as pd
from board import Board
from experiment import Experiment
import time

def main(input_file, amount_of_moves, output_folder):

    # reads the csv and turns it into a dataframe
    csv = pd.read_csv(input_file) 

    # creates a object of the class Board 
    board = Board(input_file, csv, True)
    
    board.draw() 

    experiment = Experiment(board, amount_of_moves, input_file, output_folder)
    experiment.start_random_experiment()

    time.sleep(12)


if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "reads in csv file")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")
    parser.add_argument("amount_of_moves", help = "amount of moves to try", type=int, default=10 ** 4)

    parser.add_argument("--output", help = "output folder", default = "data", required=False)

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input)
