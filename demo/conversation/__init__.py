import logging
from . import sentiment
from . import categorization
import pandas as pd


class Conversations(pd.DataFrame):
    def categorize(self, logger: logging.Logger):
        self = categorization.categorize_conversations(self, logger)

    def compute_all_sentiment_changes(self, logger: logging.Logger):
        self = sentiment.compute_all_sentiment_changes(self, logger)
