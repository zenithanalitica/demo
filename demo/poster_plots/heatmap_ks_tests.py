import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from typing import cast
import itertools
from pathlib import Path

BRITISH_AIRWAYS_ID = "18332190"

def main(df: pd.DataFrame):

    processed_df = df[['sentiment_change', 'category']].loc['18332190', slice(None), 0]

    categories = sorted(processed_df['category'].unique())
    pairs = list(itertools.combinations(categories, 2))
    m_tests = len(pairs)
    alpha = 0.05

    # Prepare an empty square DataFrame of 1.0s
    p_matrix = pd.DataFrame(
        data = np.ones((len(categories), len(categories))),
        index = categories,
        columns = categories
    )

    # Run tests and fill the df
    for cat1, cat2 in pairs:
        g1 = processed_df.loc[processed_df['category'] == cat1, 'sentiment_change']
        g2 = processed_df.loc[processed_df['category'] == cat2, 'sentiment_change']
        
        ks_stat, raw_p = stats.ks_2samp(g1, g2)
        bonf_p = min(raw_p * m_tests, 1.0) # <-- multiply by m, cap at 1
        
        p_matrix.at[cat1, cat2] = bonf_p
        p_matrix.at[cat2, cat1] = bonf_p

    # Heatmap
    plt.figure(figsize=(9, 7))
    sns.heatmap(
        p_matrix,
        annot=True,
        fmt=".3f",
        cmap='viridis_r',
        vmin=0, vmax=1,
        linewidths=0.5
    )
    plt.title('Pairwise KS Test P-Values\n(Bonferroni Corrected)', fontsize=14)
    plt.xlabel('Category')
    plt.ylabel('Category')
    plt.tight_layout()

    Path("output").mkdir(parents=True, exist_ok=True)
    
    plt.savefig('output/heatmap_ks.png')

    
if __name__ == "__main__":
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
