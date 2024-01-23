import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('random_experiments.csv')

df_sorted = df.sort_values(by='move', ascending=False)

plt.figure(figsize=(20,10))

# makes the plot with the information from the dataframe
plt.hist(df, bins=30, color='skyblue', edgecolor='black')

mean = df['move'].mean()

plt.axhline(y=mean, color='black', label='Mean move')
            
plt.xlabel("Amount of experiments")
plt.ylabel("Made moves")
plt.title("Random Experiment results")


plt.savefig('graph-mean-sorted.png')