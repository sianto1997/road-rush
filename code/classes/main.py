import argparse
import pandas as pd
from experiment import Experiment, MoveMethods

def main(input, amount_of_moves, output_directory, amount_of_experiments, move_method, save_threshold, output_check50):
    """
    Main function the program.

    Input:
    - input: Filename of board
    - amount_of_moves: Amount of moves before cut_off of the experiment
    - output_directory: Which folder to save the moves to
    - move_method: Way to move
    """
    # reads the csv and turns it into a dataframe
    csv = pd.read_csv(input) 

    experiment = Experiment(amount_of_moves, amount_of_experiments, input, output_directory, output_check50)
    experiment.start_random_experiment(input, csv, move_method, save_threshold)

if __name__ == "__main__":
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "reads in csv file")

    # Adding arguments
    parser.add_argument("input", help = "input file (csv)")
    parser.add_argument("--amount_of_moves", help = "amount of moves to try", required=False, type=int, default=1000)
    parser.add_argument("--output_directory", help = "output directory", required=False, default = "output")
    parser.add_argument("--amount_of_experiments", help = "amount of experiments to try", required=False, type=int, default=1)
    parser.add_argument("--move_method", help = "move method (0 = RandomMax, 1 = RandomOne, 2 = RandomTwo), default is RandomMax", required=False, type=int, default=0)
    parser.add_argument("--save_threshold", help = "save run of the experiment when amount of moves is at or below number (default=100) ", required=False, type=int, default=100)
    parser.add_argument("--output_check50", help = "save as output.csv (used for check50)", required=False, type=bool, default=False)

    # Read arguments from command line
    args = parser.parse_args()
    print(args)

    # Run main with provide arguments
    main(args.input, args.amount_of_moves, args.output_directory, args.amount_of_experiments, args.move_method, args.save_threshold, args.output_check50)
