import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def get_sentiment(df):
    sid = SentimentIntensityAnalyzer()
    df['sentiment'] = df['title'].apply(lambda x: sid.polarity_scores(x))
    df['sentiment_category'] = df['sentiment'].apply(
        lambda x: 'positive' if x['compound'] > 0.2 else 'negative' if x['compound'] < -0.2 else 'neutral')
    return df.drop(columns=['sentiment'])