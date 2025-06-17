from typing import cast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BRITISH_AIRWAYS_ID = "18332190"

def main():

    category_order = sorted(df['category'].unique())
    df = df.reset_index()
    df["airline_group"] = df["airline"].apply(
        lambda x: "British Airways" if x == BRITISH_AIRWAYS_ID else "Other Airlines")

    plt.figure(figsize=(14, 8))
    sns.barplot(
        data=df,
        x='category',
        y='sentiment_change',
        hue='airline_group',
        order=category_order,
        palette={'British Airways': 'royalblue', 'Other Airlines': 'lightgray'},
        errorbar='sd'
    )
    plt.title('Average Sentiment Change: British Airways vs. Other Airlines by Category', fontsize=16)
    plt.xlabel('Topic Category', fontsize=12)
    plt.ylabel('Average Sentiment Change', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.axhline(0, color='red', linestyle='--', linewidth=1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Airline Group')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
