from pathlib import Path
from typing import cast

import matplotlib.pyplot as plt
import pandas as pd

# Load your data (update the path as needed)
# If your CSV was read with a MultiIndex, we'll reset it to access 'tweet' as a column:

df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
df = df.reset_index()


# Now identify first tweet of each conversation
first_tweets = df[df["tweet"] == 0].copy()

# Compute average sentiment score per category for first tweets (red)
base_sentiment = (
    first_tweets.groupby("category")["sentiment_score"].mean().rename("base")
)

# Compute average sentiment_change per conversation, then adjusted score per conversation
delta = (
    df.groupby(["category", "conversation"])["sentiment_change"].mean().reset_index()
)
delta = delta.merge(
    first_tweets[["category", "conversation", "sentiment_score"]],
    on=["category", "conversation"],
)
delta["adjusted"] = delta["sentiment_score"] + delta["sentiment_change"]

# Compute average adjusted score per category (blue)
adjusted_sentiment = delta.groupby("category")["adjusted"].mean().rename("adjusted")

# Combine into plotting DataFrame
plot_df = pd.concat([base_sentiment, adjusted_sentiment], axis=1).reset_index()
plot_df = plot_df.sort_values("base")

# Create dumbbell plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.hlines(
    plot_df["category"], plot_df["base"], plot_df["adjusted"], color="gray", linewidth=2
)
ax.scatter(
    plot_df["base"], plot_df["category"], color="red", label="Avg first-tweet sentiment"
)
ax.scatter(
    plot_df["adjusted"], plot_df["category"], color="blue", label="First + avg change"
)

ax.set_xlabel("Sentiment Score")
ax.set_ylabel("Category")
ax.set_title("Sentiment Shift by Category")
ax.legend()
plt.tight_layout()

# Ensure output directory exists
Path("output").mkdir(parents=True, exist_ok=True)

# Save to file
plt.savefig("output/dumbell.png")
