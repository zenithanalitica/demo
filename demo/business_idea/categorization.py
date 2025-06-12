import pandas as pd
import logging
from datetime import timedelta
import time

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "flight delays and cancellations": [
        "delay",
        "delayed",
        "cancelled",
        "cancel",
        "rescheduled",
        "late",
        "no information",
        "boarding closed",
    ],
    "baggage and check in issues": [
        "baggage",
        "luggage",
        "lost bag",
        "missing bag",
        "check-in",
        "check in",
        "boarding denied",
        "boarding closed early",
    ],
    "booking app payment problems": [
        "book",
        "booking",
        "app",
        "seat",
        "payment",
        "ticket",
        "website",
        "log in",
        "error",
    ],
    "customer service and response quality": [
        "no reply",
        "ignored",
        "unhelpful",
        "bad service",
        "rude",
        "no response",
        "dm",
        "support",
        "mail",
        "customer-service",
    ],
    "refunds and compensation requests": [
        "refund",
        "compensation",
        "claim",
        "voucher",
        "money back",
        "eu261",
        "reimbursement",
    ],
}


def assign_category_to_conv(
    conv: pd.DataFrame,
) -> pd.DataFrame:
    text = str(conv.iloc[0]["text"]).lower()
    assigned_category = "other"  # default

    for category_name, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in text for keyword in keywords):
            assigned_category = category_name.split()[0]
            break

    conv["category"] = assigned_category
    return conv


def categorize_conversations(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    logger.info("Evaluating categories for conversations...")
    start_time = time.time()

    df_categorized = df.groupby("conversation", group_keys=False).apply(
        assign_category_to_conv, category_keywords=CATEGORY_KEYWORDS
    )

    end_time = time.time()
    logger.info(
        f"Finished evaluating categories. Time taken: {timedelta(seconds=end_time - start_time)}"
    )
    return df_categorized

