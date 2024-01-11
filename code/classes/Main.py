import argparse
import pandas as pd
from board import Board

def main(input_file):
    csv = pd.read_csv(input_file) 

    board = Board(input_file)
    board.add_cars(csv) 

    board.visualize_board() 

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "reads in csv file")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")

    # Read arguments from command line
    args = parser.parse_args()

    # Run main with provide arguments
    main(args.input)
