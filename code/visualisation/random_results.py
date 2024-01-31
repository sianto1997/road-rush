import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
def hist_plot(input_file, threshold: int, output_name: str, bar_point: int, title: str, width: int):
    '''
    Creates a histogram for the results of random

    Parameters
    ----------
    input_file : csv
        The csv with the data for the plot
    threshold : int
        The max amount of moves that are being shown in the tabel, everything above will be shown in one line
    output_name : str
        The name of the output file
    bar_point : int
        Place on the x-axis where the bar with the amount of moves above the threshold will be
    title : str
        The title above the graph
    width : int
        The width of the bar with the amount of moves above the threshold
    '''

    df = pd.read_csv(input_file)

    df_sorted = df.sort_values(by='move', ascending=False)
    df_wanted_moves = df_sorted[df_sorted['move'] <= threshold]
    df_other_moves = df_sorted[df_sorted['move'] > threshold]

    moves_above_threshold = len(df_other_moves)
    print(moves_above_threshold)

    plt.hist(df_wanted_moves['move'], bins=50, label='Moves up to threshold', rwidth= 0.7)
    plt.bar(bar_point, moves_above_threshold, width=width, log=True)
    plt.xlim(left=0,right=threshold+100)
    plt.xlabel("Amount of moves")
    plt.ylabel("Count")
    plt.title(title)

    plt.savefig(output_name)


random6x6 = hist_plot('visualisation_input/Rushhour6x6_1.csv_RandomAll_random_experiments_S2024-01-23_21-26-02_E2024-01-24_14-05-04.csv', 1000, 'random_6x6.png', 1020,"Random Experiment results 6x6", 20)
plt.show()
random9x9 = hist_plot('visualisation_input/Rushhour9x9_4.csv_RandomAll_random_experiments_S2024-01-23_21-26-02_E2024-01-24_14-05-04.csv', 5000,'random_9x9', 5020, 'Random Experiment results 9x9', 40)
plt.show()
random12x12 = hist_plot('visualisation_input/Rushhour12x12_7.csv_RandomAll_random_experiments_S2024-01-24_16-26-23_E2024-01-26_03-53-12.csv', 10000, 'random_12x12.png', 10020,'Random Experiment results 12x12', 60)