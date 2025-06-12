import logging
from . import sentiment
from . import categorization
from . import adjust
import pandas as pd
import datetime


class Conversations(pd.DataFrame):
    def adjust(
        self, start_date: datetime.date, end_date: datetime.date, logger: logging.Logger
    ):
        return Conversations(adjust.adjust_df(self, start_date, end_date, logger))

    def categorize(self, logger: logging.Logger):
        return Conversations(categorization.categorize_conversations(self, logger))

    def compute_all_sentiment_changes(self, logger: logging.Logger):
        return Conversations(sentiment.compute_all_sentiment_changes(self, logger))
