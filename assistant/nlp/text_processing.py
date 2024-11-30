import re
import spacy
from utils.logger import log

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    log(f"Error loading spaCy model: {e}", "error")
    exit(1)

def clean_text(text):
    """
    Clean and normalize the text by removing special characters, extra spaces, and converting to lowercase.
    """
    try:
        text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip().lower()
        return text
    except Exception as e:
        log(f"Error cleaning text: {e}", "error")
        return ""

def tokenize_text(text):
    """
    Tokenize the text using spaCy.
    """
    try:
        doc = nlp(text)
        tokens = [token.text for token in doc]
        return tokens
    except Exception as e:
        log(f"Error tokenizing text: {e}", "error")
        return []

if __name__ == "__main__":
    test_text = "Hello, World! This is a test message."
    print("Cleaned Text:", clean_text(test_text))
    print("Tokens:", tokenize_text(test_text))
