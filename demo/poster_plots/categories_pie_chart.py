import datetime
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import pandas as pd


def main(df: pd.DataFrame):
    df_reset = df.reset_index(level="conversation")

    result = (
        df_reset.groupby("category")["conversation"]
        .nunique()
        .reset_index(name="conversation_count")
        .sort_values("category")
    )

    categories = result.category
    values = result.conversation_count

    colors = ["#6a0dad", "#7b68ee", "#9370db", "#6495ed", "#00bfff", "#4169e1"]

    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=categories, autopct="%1.1f%%", startangle=90, colors=colors)
    plt.axis("equal")

    # Ensure output directory exists
    Path("output").mkdir(parents=True, exist_ok=True)

    # Save to file
    plt.savefig("output/pie_chart.png")


if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
