import datetime
from pathlib import Path
from typing import cast

import pandas as pd
import plotly.graph_objects as go
from plotly.offline import init_notebook_mode, iplot


def main(
    df: pd.DataFrame, start_date: datetime.date | None, end_date: datetime.date | None
):
    # Reset your MultiIndex and sort by tweet order
    df_reset = df.reset_index()

    # Reset index and sort
    df_reset = df.reset_index()
    df_sorted = df_reset.sort_values(["airline", "conversation", "tweet"])

    # Filter to the airline you confirmed exists
    AIRLINE_ID = "18332190"
    df_airline = df_sorted[df_sorted["airline"] == AIRLINE_ID]

    # Compute first & last sentiments
    trans = (
        df_airline.groupby(["airline", "conversation"])["sentiment_label"]
        .agg(first="first", last="last")
        .reset_index()
    )

    # Count transitions
    counts = trans.groupby(["first", "last"]).size().reset_index(name="count")

    colors = ["#4CAF50", "#9E9E9E", "#F44336"] * 2
    first_map = {"positive": 0, "neutral": 1, "negative": 2}
    last_map = {"positive": 3, "neutral": 4, "negative": 5}
    sources = counts["first"].map(first_map)
    targets = counts["last"].map(last_map)
    values = counts["count"]
    link_colors = [colors[s] for s in sources]

    x = [0, 0, 0, 1, 1, 1]
    y = [0.9, 0.5, 0.1, 0.9, 0.5, 0.1]

    fig = go.Figure(
        go.Sankey(
            arrangement="fixed",
            node=dict(
                color=colors,
                x=x,
                y=y,
                pad=20,
                thickness=30,
                line=dict(color="black", width=1),
            ),
            link=dict(source=sources, target=targets, value=values, color=link_colors),
        )
    )

    date = f" between {start_date} and {end_date}" if start_date is not None else ""
    fig.update_layout(
        title_text=f"Sentiment Transition for British Airways{date}",
        width=630,
        height=600,
        margin=dict(l=50, r=50, t=80, b=50),
        plot_bgcolor="white",
    )

    # Ensure output directory exists
    Path("output").mkdir(parents=True, exist_ok=True)

    # Save to file
    fig.write_html("output/sankey.html")


if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df)
