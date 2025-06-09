import pandas as pd
import numpy as np

df = pd.read_pickle('./conversations.pkl')

def compute_change(conv: pd.DataFrame):
    initial: int = conv.iloc[0]['sentiment_score']
    latter: int = np.mean(conv.iloc[2:]['sentiment_score'])

    conv['sentiment_change'] = latter - initial
    return conv

#Applying analysis function to the df
df = df.groupby('conversation', group_keys=False).apply(compute_change)

df.to_pickle('sentiment_conversations.pkl')

df.head(20)