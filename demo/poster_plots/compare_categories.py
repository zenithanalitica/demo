from typing import cast
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

from scipy import stats

BRITISH_AIRWAYS_ID = "18332190"


def main(df: pd.DataFrame):
    # Calculate performance metrics for each category
    performance_results = []
    df = df.reset_index()
    df["airline_group"] = df["airline"].apply(
        lambda x: "British Airways" if x == BRITISH_AIRWAYS_ID else "Other Airlines"
    )

    for category in df["category"].unique():
        category_data = df[df["category"] == category]

        target_data = category_data[
            category_data["airline_group"] == "British Airways"
        ]["sentiment_change"]
        others_data = category_data[category_data["airline_group"] == "Other Airlines"][
            "sentiment_change"
        ]

        if len(target_data) == 0 or len(others_data) == 0:
            print("no data")
            continue

        # Calculate metrics
        target_mean = target_data.mean()
        others_mean = others_data.mean()
        target_median = target_data.median()
        others_median = others_data.median()

        # Performance comparison
        mean_difference = target_mean - others_mean
        median_difference = target_median - others_median

        # Effect size (Cohen's d)
        pooled_std = np.sqrt(
            (
                (len(target_data) - 1) * target_data.std() ** 2
                + (len(others_data) - 1) * others_data.std() ** 2
            )
            / (len(target_data) + len(others_data) - 2)
        )
        cohens_d = mean_difference / pooled_std if pooled_std > 0 else 0

        # Statistical significance (t-test)
        t_stat, p_value = stats.ttest_ind(target_data, others_data)

        performance_results.append(
            {
                "category": category,
                "target_mean": target_mean,
                "others_mean": others_mean,
                "target_median": target_median,
                "others_median": others_median,
                "mean_difference": mean_difference,
                "median_difference": median_difference,
                "cohens_d": cohens_d,
                "p_value": p_value,
                "target_n": len(target_data),
                "others_n": len(others_data),
                "performance": "Better" if mean_difference > 0 else "Worse",
                "significant": p_value < 0.05,
            }
        )

    perf_df = pd.DataFrame(performance_results)

    # Sort by mean difference for better visualization
    perf_df = perf_df.sort_values("mean_difference", ascending=True)
    perf_df["percent_difference"] = (
        100 * perf_df["mean_difference"] / perf_df["others_mean"]
    )

    # Create comprehensive visualization
    fig, ax1 = plt.subplots(1, 1, figsize=(16, 12))

    # 1. MEAN DIFFERENCE PLOT (Main visualization)
    colors = [
        "#e74c3c" if diff < 0 else "#27ae60" for diff in perf_df["mean_difference"]
    ]
    bars = ax1.barh(
        perf_df["category"],
        perf_df["percent_difference"],
        color=colors,
        alpha=0.8,
        edgecolor="black",
    )
    ax1.set_xlabel(
        "Mean Sentiment Change (% Difference vs Other Airlines)",
        fontsize=12,
        fontweight="bold",
    )

    # Add zero line
    ax1.axvline(x=0, color="black", linestyle="-", alpha=0.8, linewidth=2)

    # Add significance stars
    for i, (idx, row) in enumerate(perf_df.iterrows()):
        x_pos = row["mean_difference"] + (0.01 if row["mean_difference"] > 0 else -0.01)
        if row["significant"]:
            if row["p_value"] < 0.001:
                stars = "***"
            elif row["p_value"] < 0.01:
                stars = "**"
            else:
                stars = "*"
            ax1.text(
                x_pos,
                i,
                stars,
                va="center",
                ha="left" if row["mean_difference"] > 0 else "right",
                fontweight="bold",
                fontsize=12,
            )

    # ax1.set_xlabel('Mean Sentiment Change Difference\n(British Airways - Other Airlines)', fontsize=12, fontweight='bold')
    ax1.set_title(
        "British Airways Performance by Category", fontsize=14, fontweight="bold"
    )
    ax1.set_xlim([-20, 20])
    ax1.grid(axis="x", alpha=0.3)

    # Add performance labels
    ax1.text(
        0.02,
        len(perf_df) - 0.5,
        "BETTER →",
        fontsize=12,
        fontweight="bold",
        color="#27ae60",
        alpha=0.8,
    )
    ax1.text(
        -0.005,
        len(perf_df) - 0.5,
        "← WORSE",
        fontsize=12,
        fontweight="bold",
        color="#e74c3c",
        alpha=0.8,
        ha="right",
    )

    plt.savefig("output/category_diff.png")


if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
