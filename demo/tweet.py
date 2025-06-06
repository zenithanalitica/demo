from dataclasses import dataclass
from datetime import date


@dataclass
class Tweet:
    id: str
    sentiment_label: str
    sentiment_score: float
    created_at: date
    negative: float
    neutral: float
    positive: float
    reply_to: str | None = None
