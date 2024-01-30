# Mijn Project

Hier staat een korte beschrijving van het probleem evt. met plaatje.

## Getting Started

### Prerequisites

This codebase is written completely in [Python3.11.5](https://www.python.org/downloads/). In requirements.txt all required packages to run the code succesfully are mentioned. These can be installed via pip by executing the following statement:

```
pip install -r requirements.txt
```

### Structure

Alle Python scripts staan in de folder Code. In de map Data zitten alle input waardes en in de map resultaten worden alle resultaten opgeslagen door de code.

### Testing

To run the code with the default configuration (algorithm Random, board Rushhour6x6_1.csv) use de statement:

```
python main.py data/Rushhour6x6_1.csv --amount_of_experiments 1000
```
This will output the top 5 solutions the Random algorithm has found. It will also save a summary



## Auteurs (Authors)

* Amber Korte
* Esmée de Roo
* Simon Antonides

## Dankwoord (Acknowledgments)

* StackOverflow
* minor AI van de UvA
