from datetime import timedelta
import logging
import os
import time
from typing import cast
import pandas as pd
import libs.conversation_store as convstr


class App:
    def __init__(self) -> None:
        self.conversations: pd.DataFrame = load_conversations()

    def run(self) -> None:
        pass


def load_conversations() -> pd.DataFrame:
    if not os.path.isfile("./conversations.pkl"):
        start_time = time.time()
        logging.info("Conversations not cached. Fetching from database...")
        convstr.load_conversations()
        logging.info(
            f"Conversations fetched. Time taken: {str(timedelta(seconds=time.time() - start_time))}"
        )

    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    return df
