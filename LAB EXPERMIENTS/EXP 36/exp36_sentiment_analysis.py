import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download required package data; safe to run repeatedly
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon", quiet=True)

sia = SentimentIntensityAnalyzer()
texts = [
    "I absolutely love this new feature! It is amazing.",
    "This is the worst experience I have ever had.",
    "The product is okay, neither good nor bad.",
]

for text in texts:
    scores = sia.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        label = "Positive"
    elif compound <= -0.05:
        label = "Negative"
    else:
        label = "Neutral"

    print(f"Text: {text}")
    print(f"Sentiment: {label}")
    print(f"Scores: {scores}\n")
