from typing import cast
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

BRITISH_AIRWAYS_ID = "18332190"


def main(df: pd.DataFrame):
    df = df.reset_index()
    # Create a new column to distinguish between target user and others
    df["airline_group"] = df["airline"].apply(
        lambda x: "British Airways" if x == BRITISH_AIRWAYS_ID else "Other Airlines"
    )

    # Get unique categories
    categories = df["category"].unique()
    n_categories = len(categories)

    # Set up the plot
    fig, axes = plt.subplots(
        n_categories, 1, figsize=(4 * n_categories, 6), sharey=True
    )

    # Create violin plots for each category
    for i, category in enumerate(categories):
        # Filter data for current category
        category_data = df[df["category"] == category]

        # Create violin plot
        sns.violinplot(
            data=category_data,
            x="airline_group",
            y="sentiment_change",
            ax=axes[i],
            hue="airline_group",
        )

        # Customize the subplot
        axes[i].set_title(f"Category: {category}", fontsize=12, fontweight="bold")
        axes[i].set_xlabel("Airline", fontsize=10)
        axes[i].tick_params(axis="x", rotation=45)

        # Only show y-label on the first subplot
        if i == 0:
            axes[i].set_ylabel("Sentiment Change", fontsize=10)
        else:
            axes[i].set_ylabel("")

    # Adjust layout
    plt.tight_layout()
    plt.suptitle(
        "Sentiment Change Distribution: British Airways vs other airlines",
        fontsize=14,
        fontweight="bold",
        y=1.0,
    )

    # Show the plot
    plt.savefig("output/violins.png")

    # # Optional: Print summary statistics
    # print("\nSummary Statistics by Category and User Group:")
    # print("=" * 60)
    # summary_stats = (
    #     df.groupby(["category", "airline_group"])["sentiment_change"]
    #     .agg(["count", "mean", "median", "std"])
    #     .round(3)
    # )
    # print(summary_stats)
    # print(df["airline_group"].head())


if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
