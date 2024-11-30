from transformers import pipeline
from utils.logger import log

# Load Hugging Face sentiment analysis pipeline
try:
    sentiment_pipeline = pipeline("sentiment-analysis")
except Exception as e:
    log(f"Error loading sentiment analysis model: {e}", "error")
    exit(1)

def analyze_sentiment(text):
    """
    Analyze the sentiment of the given text.
    """
    try:
        result = sentiment_pipeline(text)
        return result[0]  # Return label and score
    except Exception as e:
        log(f"Error analyzing sentiment: {e}", "error")
        return {"label": "Error", "score": 0.0}

if __name__ == "__main__":
    test_text = "I love this project!"
    print("Sentiment Analysis:", analyze_sentiment(test_text))
