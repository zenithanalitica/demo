import logging
import os
import time
from datetime import timedelta
from typing import cast

import convstr
import pandas as pd

from . import conversation as conv


class App:
    def __init__(self) -> None:
        self.logger: logging.Logger = create_logger()
        self.conversations: conv.Conversations = conv.Conversations(
            load_conversations(self.logger)
        )

    def run(self) -> None:
        # Process data
        self.conversations.categorize(self.logger)
        self.conversations.compute_all_sentiment_changes(self.logger)


def load_conversations(logger: logging.Logger) -> pd.DataFrame:
    if not os.path.isfile("./conversations.pkl"):
        start_time = time.time()
        logger.info("Conversations not cached. Fetching from database...")
        convstr.load_conversations(logger)
        logger.info(
            f"Conversations fetched. Time taken: {str(timedelta(seconds=time.time() - start_time))}"
        )
    else:
        logger.info("Found a cached conversation file.")

    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    return df


def create_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    # Create a console handler and set its level
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger
