import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('random_experiments.csv')

plt.figure(figsize=(20,10))

# makes the plot with the information from the dataframe
plot = sns.barplot(data = df, x=, y='move')

# makes sure the labels are at an angle and that they are readable
plot.set_xticklabels(plot.get_xticklabels(), rotation=40, ha="right")
plt.tight_layout()

# saves the outcome of the plot into a png file
plt.savefig(output_file)