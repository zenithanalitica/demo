import argparse
import logging
import os
import time
from datetime import timedelta, date
from typing import cast

import convstr
import pandas as pd

from . import conversation as conv
from . import poster_plots as plots


class App:
    def __init__(self) -> None:
        self.logger: logging.Logger = create_logger()
        self.conversations: conv.Conversations = conv.Conversations(
            load_conversations(self.logger)
        )
        self.start_date: date | None = None
        self.end_date: date | None = None
        self.parse_args()

    def run(self) -> None:
        # Process data
        self.conversations = self.conversations.adjust(
            self.start_date, self.end_date, self.logger
        )
        self.conversations = self.conversations.categorize(self.logger)
        self.conversations = self.conversations.compute_all_sentiment_changes(
            self.logger
        )

        plots.dumbell.main(self.conversations)
        plots.sankey.main(self.conversations)
        plots.violins_by_category.main(self.conversations)

        if self.start_date is None and self.end_date is None:
            self.save_df()

    def parse_args(self):
        # Initialize parser
        parser = argparse.ArgumentParser(
            prog="demo", description="Demo for app", exit_on_error=True
        )

        # Add arguments
        _ = parser.add_argument(
            "--start-date",
            type=str,
            help="Start date of the desired period in YYYY-MM-DD format",
            default="",
        )
        _ = parser.add_argument(
            "--end-date",
            type=str,
            help="End date of the desired period in YYYY-MM-DD format",
            default="",
        )

        # Read arguments from command line and cast them to Args class
        args = parser.parse_args()

        if cast(str, args.start_date) == "" or cast(str, args.end_date) == "":
            return

        self.start_date = date.fromisoformat(cast(str, args.start_date))
        self.end_date = date.fromisoformat(cast(str, args.end_date))

    def save_df(self) -> None:
        file = "./conversations.pkl"
        self.logger.info(f"Saving data frame to the {file}")
        pd.to_pickle(self.conversations, file)


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
