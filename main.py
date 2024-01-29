import argparse
from code.classes.runner import Runner
from code.algorithms.random import Random, MoveMethods
from code.algorithms.amber_manual import AmberManual
from code.algorithms.greedy import Greedy
from code.algorithms.breadthfirst import BreadthFirst
from code.algorithms.branch_bound import BranchAndBound

import pickle

def main(input, algorithm, amount_of_moves, output_directory, amount_of_experiments, move_method, save_threshold, output_check50, visualize, draw_interval, resume):
    '''
    Main function the program.

    Input:
    - input (string): Filename of board
    - amount_of_moves (int): Amount of moves before cut_off of the experiment
    - output_directory (string): Which folder to save the moves to
    - move_method (int): Way to move
    - save_threshold (int): Save solutions only when at or lower than threshold
    - output_check50 (bool): Save as output.csv to satisfy check50 required output filename
    - visualize (bool): Show visualization (disabled by default)
    - draw_interval (float): The interval between moves in the visualization
    - resume (bool): Resume previous experiment
    '''

    kwargs = {}
    if move_method >= 0:
        kwargs['move_method'] = move_method

    if not resume:
        runner = Runner(amount_of_moves, amount_of_experiments, input, output_directory, output_check50, visualize, draw_interval, switch(algorithm), save_threshold, **kwargs)
    else:
        file_name = input.split('/')[-1]
        with open(f'../{file_name}.pickle', 'rb') as pickle_file:
            runner = pickle.load(pickle_file)

    runner.run()

def switch(algorithm = ''):
    '''
    This function acts as a switch case for selecting an algorithm in prompt.
    
    Input:
    - algorithm (string): The name of a specific algorithm (default '').

    Output:
    - algorithm (Algorithm): The algorithm to be used. If no suitable algorithm is found Random will be returned.

    '''
    if algorithm == 'Greedy':
        return Greedy
    elif algorithm == 'BreadthFirst':
        return BreadthFirst
    elif algorithm == 'BranchAndBound':
        return BranchAndBound
    elif algorithm == 'AmberManual':
        return AmberManual
    else:
        return Random


if __name__ == "__main__":
    '''
    The portion called when the main.py is called on directly.
    '''
    # Set-up parsing command line arguments
    parser = argparse.ArgumentParser(description = "Reads in csv file")

    # Adding arguments
    parser.add_argument("input", help = "Input file (csv)")
    parser.add_argument("--algorithm", help = "The algorithm to use for the experiment", required=False, type=str, default='')
    parser.add_argument("--amount_of_moves", help = "Amount of moves to try (0 is unlimited)", required=False, type=int, default=0)
    parser.add_argument("--output_directory", help = "Output directory", required=False, default = "output")
    parser.add_argument("--amount_of_experiments", help = "Amount of experiments to try", required=False, type=int, default=1)
    parser.add_argument("--move_method", help = "Move method (0 = RandomAll, 1 = RandomOne, 2 = RandomTwo), default is RandomAll", required=False, type=int, default=-1)
    parser.add_argument("--save_threshold", help = "Save run of the experiment when amount of moves is at or below number (default=100). Input of 0 means save all.", required=False, type=int, default=100)
    parser.add_argument("--output_check50", help = "Save as output.csv (used for check50)", required=False, type=bool, default=False)
    parser.add_argument("--visualize", help = "Show visual board", required=False, type=bool, default=False)
    parser.add_argument("--resume", help = "Resume previous experiment", required=False, type=bool, default=False)
    parser.add_argument("--draw_interval", help = "Resume previous experiment", required=False, type=float, default=0.01)

    # Read arguments from command line 
    args = parser.parse_args()
    print(args)

    # Run main with provide arguments
    main(args.input, args.algorithm, args.amount_of_moves, args.output_directory, args.amount_of_experiments, args.move_method, args.save_threshold, args.output_check50, args.visualize, args.draw_interval, args.resume)
