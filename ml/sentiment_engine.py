
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
_vader = SentimentIntensityAnalyzer()
def sentiment_textblob(text: str) -> dict:
    b = TextBlob(text)
    return {"polarity": float(b.sentiment.polarity), "subjectivity": float(b.sentiment.subjectivity)}
def sentiment_vader(text: str) -> dict:
    s = _vader.polarity_scores(text)
    return {"compound": float(s["compound"]), "pos": float(s["pos"]), "neu": float(s["neu"]), "neg": float(s["neg"])}
