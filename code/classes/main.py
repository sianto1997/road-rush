import argparse
import pandas as pd
from board import Board
from experiment import Experiment
import time

def main(input, amount_of_moves, output_directory):
    """
    Main function the program.

    Input:
    - input: Filename of board
    - amount_of_moves: Amount of moves before cut_off of the experiment
    - output_directory: Which folder to save the moves to
    """
    # reads the csv and turns it into a dataframe
    csv = pd.read_csv(input) 

    # creates a object of the class Board 
    board = Board(input, csv)
    
    board.draw() 

    experiment = Experiment(board, amount_of_moves, input, output_directory)
    experiment.start_random_experiment()

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "reads in csv file")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")
    parser.add_argument("--amount_of_moves", help = "amount of moves to try", required=False, type=int, default=1000)
    parser.add_argument("--output_directory", help = "output directory", required=False, default = "output")

    # Read arguments from command line
    args = parser.parse_args()
    print(args)

    # Run main with provide arguments
    main(args.input, args.amount_of_moves, args.output_directory)
