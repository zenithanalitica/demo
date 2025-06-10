import pandas as pd
import logging

from . import categorization
from . import sentiment

INPUT_PICKLE_PATH = r'.\business-idea\conversations.pkl'
OUTPUT_PICKLE_PATH = 'processed_conversations.pkl'

def main():

    logger = create_logger()

    # Load data
    df = pd.read_pickle(INPUT_PICKLE_PATH)
    logger.info('Data loaded successfully.')

    # Process data
    df = categorization.categorize_conversations(df, categorization.category_keywords, logger)
    df = sentiment.compute_all_sentiment_changes(df, logger)

    # Save data
    logger.info(f'Saving DataFrame to {OUTPUT_PICKLE_PATH}...')
    df.to_pickle(OUTPUT_PICKLE_PATH)
    logger.info('DataFrame saved successfully.')


def create_logger() -> logging.Logger:
    logger: logging.Logger = logging.getLogger("logger")
    logger.setLevel(logging.DEBUG)

    if logger.hasHandlers():
        logger.handlers.clear()

    # Create a console handler and set its level
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)

    # Create a formatter
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(handler)

    return logger


if __name__ == '__main__':
    main()