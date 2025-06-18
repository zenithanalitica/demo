import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt
from typing import cast
import itertools

BRITISH_AIRWAYS_ID = "18332190"

def main(df: pd.DataFrame):

    processed_df = df[['sentiment_change', 'category']].loc['18332190', slice(None), 0]
    print("--- Analysis will be performed on the full filtered population ---")

    print("\n" + "="*60)
    print("Pairwise KS Tests for Overall Distribution Shape with Heatmap")
    print("="*60)

    unique_categories = sorted(processed_df['category'].unique())
    pairs = list(itertools.combinations(unique_categories, 2))
    num_comparisons = len(pairs)
    alpha = 0.05

    print(f"Performing {num_comparisons} pairwise KS tests with Bonferroni correction...")

    #Store results in a list of dictionaries to build the heatmap matrix
    p_values_ks = []

    for cat1, cat2 in pairs:
        group1 = processed_df['sentiment_change'][processed_df['category'] == cat1]
        group2 = processed_df['sentiment_change'][processed_df['category'] == cat2]
        
        # Perform the two-sample KS test
        ks_stat, p_val_ks = stats.ks_2samp(group1, group2)
        
        # Apply Bonferroni correction
        corrected_p = min(p_val_ks * num_comparisons, 1.0)
        
        # Store the result for the matrix (and its mirror image)
        p_values_ks.append({'cat1': cat1, 'cat2': cat2, 'p_value': corrected_p})
        p_values_ks.append({'cat1': cat2, 'cat2': cat1, 'p_value': corrected_p})

    #Heatmap

    p_values_df = pd.DataFrame(p_values_ks)

    #Pivot the DataFrame to create the square matrix needed for the heatmap
    heatmap_matrix = p_values_df.pivot(index='cat1', columns='cat2', values='p_value')

    #Fill the diagonal with 1.0 for clarity (a category is identical to itself)
    np.fill_diagonal(heatmap_matrix.values, 1.0)

    #Generate the heatmap
    plt.figure(figsize=(9, 7))
    sns.heatmap(heatmap_matrix, annot=True, cmap='viridis_r', fmt=".3f", linewidths=.5)
    plt.title('Pairwise KS Test P-Values for Distribution Shape\n(Bonferroni Corrected)', fontsize=14)
    plt.xlabel('Category')
    plt.ylabel('Category')
    plt.show()

    # --- Optional: Print a text summary of significant pairs ---
    print("\n--- Summary of Significant Differences in Distribution Shape (p < 0.05) ---")
    is_any_significant = False
    for i in range(len(heatmap_matrix.columns)):
        for j in range(i + 1, len(heatmap_matrix.columns)):
            p_val = heatmap_matrix.iloc[j, i] # Check the lower-left triangle
            if p_val < alpha:
                is_any_significant = True
                cat1 = heatmap_matrix.columns[i]
                cat2 = heatmap_matrix.columns[j]
                print(f"'{cat1}' vs '{cat2}': Distributions are SIGNIFICANTLY DIFFERENT (p = {p_val:.4g})")

    if not is_any_significant:
        print("No pairs with significantly different distributions were found after correction.")

    
if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
