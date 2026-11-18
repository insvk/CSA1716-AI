# Note: Requires nltk library (pip install nltk)
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon if not already downloaded
nltk.download('vader_lexicon', quiet=True)

sia = SentimentIntensityAnalyzer()

texts = [
    "I absolutely love this new feature! It's amazing.",
    "This is the worst experience I have ever had.",
    "The product is okay, neither good nor bad."
]

for text in texts:
    sentiment = sia.polarity_scores(text)
    print(f"Text: {text}")
    print(f"Sentiment Scores: {sentiment}\n")