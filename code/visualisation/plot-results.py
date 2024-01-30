import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('random_experiments.csv')

df_sorted = df.sort_values(by='move', ascending=False)

# makes the plot with the information from the dataframe
test = plt.hist(df, bins=500, color='skyblue')

mean = df['move'].mean()
min = df['move'].min()
print(min)

plt.axvline(mean, color='k', label='Mean move', linestyle='dashed', linewidth=1)
            
plt.xlabel("Amount of moves")
plt.ylabel("Count")
plt.title("Random Experiment results")


plt.savefig('hist-random-results.png')