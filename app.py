from logging import error
import os
from typing import cast
import pandas as pd


class App:
    def __init__(self) -> None:
        self.conversations: pd.DataFrame = load_conversations()

    def run(self) -> None:
        pass


def load_conversations() -> pd.DataFrame:
    if not os.path.isfile("./conversations.pkl"):
        error("Pickle file doesn't exist")
        exit()

    df = cast(pd.DataFrame, pd.read_pickle("./conversations.pkl"))
    return df
