from pathlib import Path
from typing import cast

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot

# Reset your MultiIndex and sort by tweet order
df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
df_reset = (
    df.reset_index()
)  # assumes df is indexed by ['airline','conversation','tweet']
df_sorted = df_reset.sort_values(["airline", "conversation", "tweet"])

# Extract first sentiment_label and compute average sentiment_score from the 3rd tweet onward
first = df_sorted[
    df_sorted["tweet"]
    == df_sorted.groupby(["airline", "conversation"])["tweet"].transform("min")
].set_index(["airline", "conversation"])["sentiment_label"]
avg_scores = (
    df_sorted[df_sorted["tweet"] >= 2]
    .groupby(["airline", "conversation"])["sentiment_score"]
    .mean()
    .rename("avg_sentiment_score")
)

# Combine and threshold back into labels
trans = first.to_frame().join(avg_scores, how="inner").reset_index()


def score_to_label(s):
    if s < -0.4:
        return "negative"
    if s <= 0.3:
        return "neutral"
    return "positive"


trans["avg_label"] = trans["avg_sentiment_score"].apply(score_to_label)

# Count transitions from first → average
counts = (
    trans.groupby(["sentiment_label", "avg_label"]).size().reset_index(name="count")
)

# Define fixed node labels and colors
labels = [
    "Positive\n(first)",
    "Neutral\n(first)",
    "Negative\n(first)",
    "Positive\n(avg)",
    "Neutral\n(avg)",
    "Negative\n(avg)",
]
node_colors = ["#4CAF50", "#9E9E9E", "#F44336"] * 2
first_idx = {"positive": 0, "neutral": 1, "negative": 2}
avg_idx = {"positive": 3, "neutral": 4, "negative": 5}

sources = counts["sentiment_label"].map(first_idx)
targets = counts["avg_label"].map(avg_idx)
values = counts["count"]
link_colors = [node_colors[src] for src in sources]

# Set node positions: positive top (0.95), neutral middle (0.5), negative bottom (0.05)
x = [0, 0, 0, 1, 1, 1]
y = [0.95, 0.5, 0.05, 0.95, 0.5, 0.05]

# Build the Sankey diagram
fig = go.Figure(
    go.Sankey(
        arrangement="fixed",
        node=dict(
            label=labels,
            color=node_colors,
            x=x,
            y=y,
            pad=20,
            thickness=30,
            line=dict(color="black", width=1),
            hovertemplate="%{label}<extra></extra>",
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=link_colors,
            hovertemplate="%{value} conversations<extra></extra>",
        ),
    )
)

# Force a square layout
fig.update_layout(
    title_text="Sentiment Transition: First Tweet → Avg(3rd+) Tweet",
    width=600,
    height=600,
    font=dict(size=14, family="Arial"),
    margin=dict(l=50, r=50, t=80, b=50),
    plot_bgcolor="white",
)

# Ensure output directory exists
Path("output").mkdir(parents=True, exist_ok=True)

# Save to file
fig.write_image("output/sankey.png")
