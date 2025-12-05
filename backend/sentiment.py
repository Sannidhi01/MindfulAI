# sentiment_analysis.py – Sentiment Prediction Utility
from transformers import pipeline

# Load the sentiment-analysis pipeline with a specific model
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

# Function to analyze sentiment
def analyze_sentiment(text: str):
    if not text or not text.strip():
        return {"label": "NEUTRAL", "score": 0.0}

    result = sentiment_pipeline(text[:512])[0] #limiting tokens
    return {
        "label": result["label"],
        "score": round(result["score"], 4)
    }