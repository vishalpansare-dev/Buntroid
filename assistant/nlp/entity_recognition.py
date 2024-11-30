from spacy import displacy
from utils.logger import log
import spacy

# Load spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
except Exception as e:
    log(f"Error loading spaCy model: {e}", "error")
    exit(1)

def extract_entities(text):
    """
    Extract named entities from the text using spaCy.
    """
    try:
        doc = nlp(text)
        entities = [{"text": ent.text, "label": ent.label_} for ent in doc.ents]
        return entities
    except Exception as e:
        log(f"Error extracting entities: {e}", "error")
        return []

if __name__ == "__main__":
    test_text = "Barack Obama was the 44th President of the United States."
    print("Extracted Entities:", extract_entities(test_text))
