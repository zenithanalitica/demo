import datetime
from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import pandas as pd


def main(
    df: pd.DataFrame, start_date: datetime.date | None, end_date: datetime.date | None
):
    # If your CSV was read with a MultiIndex, we'll reset it to access 'tweet' as a column:
    df_british_airways = df.loc["18332190"]
    df = df_british_airways.reset_index()

    first_tweets = df[df["tweet"] == 0].copy()

    base_sentiment = (
        first_tweets.groupby("category")["sentiment_score"].mean().rename("base")
    )

    delta = (
        df.groupby(["category", "conversation"])["sentiment_change"]
        .mean()
        .reset_index()
    )
    delta = delta.merge(
        first_tweets[["category", "conversation", "sentiment_score"]],
        on=["category", "conversation"],
    )
    delta["adjusted"] = delta["sentiment_score"] + delta["sentiment_change"]

    adjusted_sentiment = delta.groupby("category")["adjusted"].mean().rename("adjusted")

    plot_df = pd.concat([base_sentiment, adjusted_sentiment], axis=1).reset_index()
    plot_df = plot_df.sort_values("base")

    _, ax = plt.subplots(figsize=(10, 6))
    ax.hlines(
        plot_df["category"],
        plot_df["base"],
        plot_df["adjusted"],
        color="gray",
        linewidth=2,
    )
    ax.scatter(
        plot_df["base"],
        plot_df["category"],
        color="red",
        label="Average first tweet sentiment",
    )
    ax.scatter(
        plot_df["adjusted"],
        plot_df["category"],
        color="blue",
        label="Average end of conversation sentiment",
    )

    date = f" between {start_date} and {end_date}" if start_date is not None else ""
    ax.set_xlabel("Sentiment Score")
    ax.set_ylabel("Category")
    ax.set_title(f"Sentiment Shift by Category for British Airways{date}")
    ax.legend()
    plt.tight_layout()

    # Ensure output directory exists
    Path("output").mkdir(parents=True, exist_ok=True)

    # Save to file
    plt.savefig("output/dumbell.png")


if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df, None, None)
