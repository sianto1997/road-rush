# Rush Hour

Rush hour is a fun board game, where the end goal is to get the red car out of the board. This sounds easy, however there are cars and trucks abstructing this red car. The cars can only move forwards or backward in one orientation, namely horizontal or vertical. The end goal of this project is to write a smart algorithm that can get the red car as fast as possible out of the board. 


## Getting Started

### Prerequisites

This codebase is written completely in [Python 3.11.5](https://www.python.org/downloads/). In requirements.txt all required packages to run the code succesfully are mentioned. These can be installed via pip by executing the following statement:

```
pip install -r requirements.txt
```

### Structure

All code (except main.py) is located in the folder code. In the folder Data all the input boards reside. The results of the experiments are located in the output folder.

### Testing

To run the code with the default configuration (algorithm Random, board Rushhour6x6_1.csv) use de statement:

```
python main.py data/Rushhour6x6_1.csv --amount_of_experiments 1000
```
This will output the top 5 solutions the Random algorithm has found. It will also save a summary in output/experiment_summaries with the name of the input + the start and end date.

Required argument:
- input : str

    Options:

    - data/Rushhour6x6_1.csv
    - data/Rushhour6x6_2.csv
    - data/Rushhour6x6_3.csv
    - data/Rushhour9x9_4.csv
    - data/Rushhour9x9_5.csv
    - data/Rushhour9x9_6.csv
    - data/Rushhour12x12_7.csv

Other possible arguments: 
- --algorithm : str

    The algorithm to use for the experiment (default = Random algorithm)
    - BreadthFirst

    - BranchAndBound
    
    - Greedy

    - GreedyRandom

    - GreedyDepthFirst

    - Random

    - Replay
        
        Replay a solution gathered earlier (only usable in combination with --visualize)

        Required extra parameter --replay_input

    - MBW (ManualBoardWalker) 

        Only used for visualization purposes



- --amount_of_moves : int

    Amount of moves to try (0 is unlimited) (default=0)

- --output_directory : str

    Output directory (default = "output")

- --amount_of_experiments : int

    Amount of experiments to try (default = 1)

- --move_method : int

    MoveMethod (only applicable for Random algorithm) (default = 0)
    - 0 = RandomAll (Cars move between and including - the size of the board to and including + the size of the board)
    - 1 = RandomOne (Cars can move - 1 or + 1)
    - 2 = RandomTwo (Cars can move between and including - 2 or + 2)
    - 3 = RandomThree (Cars can move between and including - 3 or + 3)

- --save_threshold : int

    Save run result (all moves) of the experiment when amount of moves is at or below number. Input of 0 means save all results. (default = 100)

- --output_check50 : bool

    Save as output.csv (used for check50) (default = False)

- --visualize : bool

    Show visual board (default = False)

- --draw_interval : float

    Draw interval for visual board (only used when visualize is True) (default = 0.01)

- --resume : bool

    Resume previous (aborted with Ctrl+C) experiment using pickle (default = False) 

- --replay_input : str

    The path and filename of a result to replay (example 'output/6x6_1/Rushhour6x6_1.csv_BreadthFirst_VisitedStates523_True_M21_S21_2024-01-30_16-24-48.csv'). 
    
    Only usable in combination with the Replay algorithm.




## Authors

* Amber Korte
* Esmée de Roo
* Simon Antonides

## Acknowledgments

* Noa & Luka (TAs)
* Minor AI - UvA (Wouter & Quinten)
* StackOverflow
