import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv('algoritmes_data.csv')

df_melted = pd.melt(df, id_vars=['Algorithm', 'Board'], value_vars=['Moves', 'States'], var_name='Results', value_name='Count')

colors = {'Moves': 'orange', 'States': 'red'}

sns.barplot(data=df_melted, x='Algorithm', y='Count', hue='Results', log=True, palette=colors)
plt.title('Results 6x6')
plt.show()

plt.savefig('plot_results_all_alg')




