import re

import pandas as pd
from operator import itemgetter
from pattern.en import spelling


def reduce_lengthening(text):
    pattern = re.compile(r"(.)\1{2,}")
    return pattern.sub(r"\1\1", text)


def correct_sentence_spelling(sentence):
    corrected_words = list(map(lambda word: correct_word_spelling(word), sentence.split()))

    return ' '.join(corrected_words)


def correct_word_spelling(word):
    return max(spelling.suggest(reduce_lengthening(word)), key=itemgetter(1))[0]


df = pd.read_csv('./data/raw/training.csv', encoding='ISO-8859-1')
df.columns = ['label', 'tweet_id', 'timestamp', 'no_query', 'user', 'text']
df = df[['label', 'timestamp', 'text']]

df['label'] = df['label'] \
    .replace(0, 'Negative') \
    .replace(4, 'Positive')

df['text'] = df['text'].apply(lambda msg: re.sub('(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', ' ', msg))
df['text'] = df['text'].apply(lambda msg: re.sub('[^0-9a-zA-Z]+', ' ', msg))
df['text'] = df['text'].apply(lambda msg: msg.lower())
df['text'] = df['text'].apply(lambda msg: correct_sentence_spelling(msg))