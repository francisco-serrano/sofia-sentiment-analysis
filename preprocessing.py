import pandas as pd
import re


df = pd.read_csv('./data/raw/training.csv', encoding='ISO-8859-1')
df.columns = ['label', 'tweet_id', 'timestamp', 'no_query', 'user', 'text']
df = df[['label', 'timestamp', 'text']]

df['label'] = df['label']\
    .replace(0, 'Negative')\
    .replace(4, 'Positive')

df['text'] = df['text'].apply(lambda msg: re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', ' ', msg))
df['text'] = df['text'].apply(lambda msg: re.sub('[^0-9a-zA-Z]+', ' ', msg))
df['text'] = df['text'].apply(lambda msg: msg.lower())