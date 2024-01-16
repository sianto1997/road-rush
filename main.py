import argparse
import pandas as pd
from code.classes.runner import Runner
from code.algorithms.random import Random, MoveMethods

def main(input, amount_of_moves, output_directory, amount_of_experiments, move_method, save_threshold, output_check50, visualize):
    """
    Main function the program.

    Input:
    - input (string): Filename of board
    - amount_of_moves (int): Amount of moves before cut_off of the experiment
    - output_directory (string): Which folder to save the moves to
    - move_method (int): Way to move
    - save_threshold (int): Save solutions only when at or lower than threshold
    - output_check50 (bool): Save as output.csv to satisfy check50 required output filename
    - visualize (bool): Show visualization (disabled by default)
    """
    # reads the csv and turns it into a dataframe
    csv = pd.read_csv(input) 

    kwargs = {}
    if move_method >= 0:
        kwargs['move_method'] = move_method

    # print(kwargs)

    runner = Runner(amount_of_moves, amount_of_experiments, input, output_directory, output_check50, visualize)
    runner.run(input, csv, Random, save_threshold, **kwargs)

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "Reads in csv file")

    # Adding arguments
    parser.add_argument("input", help = "Input file (csv)")
    parser.add_argument("--amount_of_moves", help = "Amount of moves to try (0 is unlimited)", required=False, type=int, default=0)
    parser.add_argument("--output_directory", help = "Output directory", required=False, default = "output")
    parser.add_argument("--amount_of_experiments", help = "Amount of experiments to try", required=False, type=int, default=1)
    parser.add_argument("--move_method", help = "Move method (0 = RandomAll, 1 = RandomOne, 2 = RandomTwo), default is RandomAll", required=False, type=int, default=-1)
    parser.add_argument("--save_threshold", help = "Save run of the experiment when amount of moves is at or below number (default=100) ", required=False, type=int, default=100)
    parser.add_argument("--output_check50", help = "Save as output.csv (used for check50)", required=False, type=bool, default=False)
    parser.add_argument("--visualize", help = "Show visual board", required=False, type=bool, default=False)

    # Read arguments from command line 
    args = parser.parse_args()
    print(args)

    # Run main with provide arguments
    main(args.input, args.amount_of_moves, args.output_directory, args.amount_of_experiments, args.move_method, args.save_threshold, args.output_check50, args.visualize)
