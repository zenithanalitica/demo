from datetime import timedelta
import logging
import os
import time
from typing import cast
import pandas as pd
import convstr


class App:
    def __init__(self) -> None:
        self.logger: logging.Logger = create_logger()
        self.conversations: pd.DataFrame = load_conversations(self.logger)

    def run(self) -> None:
        pass


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
