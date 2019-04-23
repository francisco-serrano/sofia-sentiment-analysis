import pandas as pd

df = pd.read_csv('./data/raw/training.csv', encoding='ISO-8859-1')
df.columns = ['label', 'tweet_id', 'timestamp', 'no_query', 'user', 'text']
df = df[['label', 'timestamp', 'text']]

df['label'] = df['label']\
    .replace(0, 'Negative')\
    .replace(4, 'Positive')


