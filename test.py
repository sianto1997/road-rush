import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('random_experiments.csv')

df_sorted = df.sort_values(by='move', ascending=False)

plt.figure(figsize=(20,10))

# makes the plot with the information from the dataframe
plot = sns.barplot(data = df_sorted, x=df.index ,y='move')

# makes sure the labels are at an angle and that they are readable
num_bars = len(df)
x_ticks = np.arange(0, num_bars, 1000)
plot.set_xticks(x_ticks)
plot.set_xticklabels(x_ticks)

plot.set_xticklabels(plot.get_xticklabels(), rotation=45, ha="right")
plt.tight_layout()
plt.xlabel("Amount of experiments")
plt.ylabel("Made moves")
plt.title("Random Experiment results")

# saves the outcome of the plot into a png file
plt.savefig('graph-sorted.png')