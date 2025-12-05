from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import numpy as np
import re

model_name = "cardiffnlp/twitter-roberta-base-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

LABELS = ['negative', 'neutral', 'positive']

# Common negation words (can be expanded)
DEFAULT_NEGATIONS = {'not', 'nor', 'never', 'neither', "isn't", "wasn't", "don't", "didn't", "can't", "won't", "shouldn't", "couldn't", "wouldn't"}

def count_negations(text: str) -> int:
    words = re.findall(r"\b\w+'\w+|\w+\b", text.lower())
    return sum(1 for word in words if word in DEFAULT_NEGATIONS)

def flip_label(label: str) -> str:
    # Flip only between positive and negative. Neutral stays.
    if label == 'positive':
        return 'negative'
    elif label == 'negative':
        return 'positive'
    return 'neutral'

def analyze_sentiment(text: str):
    if not text or not text.strip():
        return {"label": "neutral"}

    encoded_input = tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
    output = model(**encoded_input)
    scores = softmax(output.logits.detach().numpy()[0])
    top_label = LABELS[np.argmax(scores)]

    negation_count = count_negations(text)
    if negation_count >= 2:
        top_label = flip_label(top_label)

    return {"label": top_label}
