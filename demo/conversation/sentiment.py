import pandas as pd
import numpy as np
import logging
from datetime import timedelta
import time

def calculate_sentiment_change_for_conv(conv: pd.DataFrame) -> pd.DataFrame:
    initial_score = conv.iloc[0]['sentiment_score']
    latter_scores = conv.iloc[2:]['sentiment_score']

    latter_mean_score = np.mean(latter_scores)
    conv['sentiment_change'] = latter_mean_score - initial_score

    return conv


def compute_all_sentiment_changes(df: pd.DataFrame, logger: logging.Logger) -> pd.DataFrame:
    if 'sentiment' in df.columns:
        return df
    
    logger.info('Computing sentiment change for conversations...')
    start_time = time.time()
    
    df_sentiment_changed = df.groupby('conversation', group_keys=False).apply(calculate_sentiment_change_for_conv)
    
    end_time = time.time()
    logger.info(f'Finished computing sentiment change. Time taken: {timedelta(seconds=end_time - start_time)}')

    return df_sentiment_changed