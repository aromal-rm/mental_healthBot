import nltk

required_nltk_packages = ['punkt', 'averaged_perceptron_tagger']

for pkg in required_nltk_packages:
    try:
        nltk.data.find(f'tokenizers/{pkg}' if pkg == 'punkt' else f'taggers/{pkg}')
    except LookupError:
        nltk.download(pkg)

from textblob import TextBlob

def get_sentiment_score(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity
