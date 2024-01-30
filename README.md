# Rush Hour

Rush hour is a fun board game, where the end goal is to get the red car out of the board. This sounds easy, however there are cars and trucks abstructing this red car. The cars can only move forwards or backward in one orientation, namely horizontal or vertical. The end goal of this project is to write a smart algorithm that can get the red car as fast as possible out of the board. 


## Getting Started

### Prerequisites

This codebase is written completely in [Python3.11.5](https://www.python.org/downloads/). In requirements.txt all required packages to run the code succesfully are mentioned. These can be installed via pip by executing the following statement:

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



## Authors

* Amber Korte
* Esmée de Roo
* Simon Antonides

## Acknowledgments

* StackOverflow
* Noa & Luka (TAs)
* Minor AI - UvA
