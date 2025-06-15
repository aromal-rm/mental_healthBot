# from textblob import TextBlob
import nltk
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from textblob import TextBlob


def get_sentiment_score(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity
