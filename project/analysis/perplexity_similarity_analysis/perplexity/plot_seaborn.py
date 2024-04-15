import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt

# categories = ['base', 'norvig', 'funspell', 'bart']
# long = [461.787511013522, 191.93403821888538, 319.80407888582437, 156.05157340399109]
# short = [7736.254397026347, 6142.7290351407, 8689.449122792392, 10841.995344264931]
# light = [1930.290759843189, 810.1938913104251, 945.8421107219435, 1844.8247629513533]
# medium = [3419.8989599032425, 1134.709664951503, 2106.3258280108657, 2221.9799026163505]
# heavy = [2795.5261774032642, 2189.6917773352366, 3132.8650179408774, 2172.987126327613]

categories = ['base', 'bart', 'norvig', 'funspell']  
long = [461.787511013522, 156.05157340399109, 191.93403821888538, 319.80407888582437]
short = [7736.254397026347, 10841.995344264931, 6142.7290351407, 8689.449122792392]
light = [1930.290759843189, 1844.8247629513533, 810.1938913104251, 945.8421107219435]
medium = [3419.8989599032425, 2221.9799026163505, 1134.709664951503, 2106.3258280108657]
heavy = [2795.5261774032642, 2172.987126327613, 2189.6917773352366, 3132.8650179408774]

# Create a dataframe for the data
import pandas as pd

df = pd.DataFrame({
    'Categories': categories,
    'long': long,
    'short': short,
    'light': light,
    'medium': medium,
    'heavy': heavy
})

# Melt the dataframe to plot
df_melted = pd.melt(df,
                    id_vars=['Categories'],
                    var_name='Intensity',
                    value_name='Scores')

# Set the style
sns.set(style="whitegrid")

# Plot using Seaborn
plt.figure(figsize=(10, 6))
sns.barplot(x='Categories',
            y='Scores',
            hue='Intensity',
            data=df_melted,
            palette='muted')

plt.title('Comparison of perplexity', fontsize=20)
plt.legend(fontsize=18, bbox_to_anchor=(1.05, 1), loc='upper right', ncol=3)

plt.xticks(fontsize=20)

plt.tight_layout()

# # Save the plot with a specific name
plt.savefig("perplexity_seaborn")

plt.show()
