import pandas as pd
import datetime
import logging


def adjust_df(
    df: pd.DataFrame,
    start_date: datetime.date | None,
    end_date: datetime.date | None,
    logger: logging.Logger,
) -> pd.DataFrame:
    if start_date is None and end_date is None:
        logger.info("No date range specified. Using full period")
        return df

    conversations = df.xs(0, level="tweet").copy()
    conversations["created_at"] = pd.to_datetime(conversations["created_at"])

    # Clamp to begging/end for missing value
    if start_date is None:
        start_date = conversations["created_at"].dt.date.min()
    if end_date is None:
        end_date = conversations["created_at"].dt.date.max()

    # Clamp start and end date to df span
    start_date = max(start_date, conversations["created_at"].dt.date.min())
    end_date = min(end_date, conversations["created_at"].dt.date.max())

    # Mask out conversations outside specified range
    mask = (conversations["created_at"].dt.date >= start_date) & (
        conversations["created_at"].dt.date < end_date
    )

    adjusted_conv_df = conversations[mask]

    valid_conversations = adjusted_conv_df.index.get_level_values("conversation")

    adjusted_df = df[
        df.index.get_level_values("conversation").isin(valid_conversations)
    ]

    logger.info(
        f"Dates parsed succesfully. Selected period: [{start_date} -> {end_date}]"
    )

    return adjusted_df
