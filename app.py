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
    logger = logging.getLogger()
    if not os.path.isfile("./conversations.pkl"):
        start_time = time.time()
        logger.warning("Conversations not cached. Fetching from database...")
        convstr.load_conversations()
        logger.warning(
            f"Conversations fetched. Time taken: {str(timedelta(seconds=time.time() - start_time))}"
        )

    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    return df
