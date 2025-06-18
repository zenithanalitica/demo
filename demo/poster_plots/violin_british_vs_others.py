from typing import cast
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import datetime
import seaborn as sns

BRITISH_AIRWAYS_ID = "18332190"

def main(df: pd.DataFrame, start_date: datetime.date, end_date: datetime.date):

    df = df.reset_index()
    df["airline_group"] = df["airline"].apply(
        lambda x: "British Airways" if x == BRITISH_AIRWAYS_ID else "Other Airlines")

    category_order = sorted(df['category'].unique())

    plt.figure(figsize=(14, 8))
    sns.violinplot(
        data=df,
        x='category',
        y='sentiment_change',
        hue='airline_group',
        order=category_order,
        split=True, # Combines BA and Other into a single violin for direct comparison
        inner='quartile', # Shows median and quartiles inside the violin
        palette={'British Airways': 'royalblue', 'Other Airlines': 'lightgray'}
    )

    date = f" between {start_date} and {end_date}" if start_date is not None else ""
    plt.title(f'Distribution Shape: British Airways vs. Other Airlines by Category{date}', fontsize=15)

    plt.xlabel('Topic Category', fontsize=12)
    plt.ylabel('Sentiment Change', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.axhline(0, color='red', linestyle='--', linewidth=1)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend(title='Airline Group')
    plt.tight_layout()
    
    Path("output").mkdir(parents=True, exist_ok=True)
    
    plt.savefig('output/violin_vs_other.png')


if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
