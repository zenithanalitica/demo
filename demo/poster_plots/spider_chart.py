import datetime
from pathlib import Path
from typing import cast

import pandas as pd
import plotly.graph_objects as go


def main(
    df: pd.DataFrame, start_date: datetime.date | None, end_date: datetime.date | None
):
    temp = df.reset_index()

    temp["airline"] = temp["airline"].astype(str)

    temp["sentiment_change"] = pd.to_numeric(temp["sentiment_change"], errors="coerce")

    ba = (
        temp[temp["airline"] == "18332190"]
        .groupby("category")["sentiment_change"]
        .mean()
        .rename("British Airways")
    )

    others = (
        temp[temp["airline"] != "18332190"]
        .groupby("category")["sentiment_change"]
        .mean()
        .rename("Other airlines")
    )

    result = pd.concat([ba, others], axis=1)

    categories = result.index.tolist()
    ba_values = result["British Airways"].tolist()
    others_values = result["Other airlines"].tolist()

    categories += [categories[0]]
    ba_values += [ba_values[0]]
    others_values += [others_values[0]]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=ba_values, theta=categories, fill="toself", name="British Airways"
        )
    )

    fig.add_trace(
        go.Scatterpolar(
            r=others_values, theta=categories, fill="toself", name="Other Airlines"
        )
    )

    date = f" between {start_date} and {end_date}" if start_date is not None else ""
    fig.update_layout(
        title=f"British Airways vs Other Airlines{date}",
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, max(max(ba_values), max(others_values)) * 1.1],
                tickvals=[0.1, 0.2, 0.3, 0.4],
                ticktext=["0.1", "0.2", "0.3", "0.4"],
            )
        ),
        showlegend=True,
    )

    # Ensure output directory exists
    Path("output").mkdir(parents=True, exist_ok=True)

    # Save to file
    fig.write_html("output/spider.html")


if __name__ == "__main__":
    # Load your data
    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    main(df, None, None)
