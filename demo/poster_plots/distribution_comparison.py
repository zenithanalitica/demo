from typing import cast
import pandas as pd
from scipy.stats import ks_2samp
import warnings

BRITISH_AIRWAYS_ID = "18332190"


# Create a new column to distinguish between target user and others
def main(df: pd.DataFrame):
    df = df.reset_index()
    df["airline_group"] = df["airline"].apply(
        lambda x: "British Airways" if x == BRITISH_AIRWAYS_ID else "Other Airlines"
    )

    # Get unique categories
    categories = df["category"].unique()
    n_categories = len(categories)

    # Kolmogorov-Smirnov tests for each category

    warnings.filterwarnings("ignore")

    print("\nKolmogorov-Smirnov Test Results:")
    print("=" * 60)
    print(f"{'Category':<20} {'KS Statistic':<15} {'p-value':<12} {'Interpretation'}")
    print("-" * 60)

    ks_results = []
    categories = df["category"].unique()

    for category in categories:
        # Get data for current category
        category_data = df[df["category"] == category]

        # Separate target user and others
        british_airways = category_data[
            category_data["airline_group"] == "British Airways"
        ]["sentiment_change"]
        other_airlines = category_data[
            category_data["airline_group"] == "Other Airlines"
        ]["sentiment_change"]

        # Check if we have enough data for both groups
        if len(british_airways) == 0:
            print(f"{category:<20} {'N/A':<15} {'N/A':<12} No target user data")
            continue
        elif len(other_airlines) == 0:
            print(f"{category:<20} {'N/A':<15} {'N/A':<12} No other users data")
            continue
        elif len(british_airways) < 3:
            print(
                f"{category:<20} {'N/A':<15} {'N/A':<12} Too few target user samples ({len(british_airways)})"
            )
            continue

        # Perform KS test
        ks_stat, p_value = ks_2samp(british_airways, other_airlines)

        # Interpretation
        if p_value < 0.001:
            interpretation = "Highly significant***"
        elif p_value < 0.01:
            interpretation = "Very significant**"
        elif p_value < 0.05:
            interpretation = "Significant*"
        else:
            interpretation = "Not significant"

        print(f"{category:<20} {ks_stat:<15.4f} {p_value:<12.4f} {interpretation}")
        result = {
            "category": category,
            "ks_statistic": ks_stat,
            "p_value": p_value,
            "british_airways_n": len(british_airways),
            "other_airlines_n": len(other_airlines),
            "significant": p_value < 0.05,
        }

        # Store results
        ks_results.append(result)

    # Create results dataframe
    ks_df = pd.DataFrame(ks_results)

    print(
        f"\nSummary: {sum(ks_df['significant'])} out of {len(ks_df)} categories show significant differences"
    )
    print("* p < 0.05, ** p < 0.01, *** p < 0.001")

    # Optional: Print summary statistics
    print("\nSummary Statistics by Category and User Group:")
    print("=" * 60)
    summary_stats = (
        df.groupby(["category", "airline_group"])["sentiment_change"]
        .agg(["count", "mean", "median", "std"])
        .round(3)
    )
    print(summary_stats)


if __name__ == "__main__":
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
