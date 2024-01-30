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




## Authors

* Amber Korte
* Esmée de Roo
* Simon Antonides

## Acknowledgments

* StackOverflow
* Noa & Luka (TAs)
* Minor AI - UvA
