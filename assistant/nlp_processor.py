from transformers import pipeline

# Load NLP model
nlp_model = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

# Determine user intent
intent_model = pipeline("zero-shot-classification")

# List of possible intents
intents = [
    "ask_time",
    "ask_date",
    "check_email",
    "create_directory",
    "delete_directory",
    "search_file",
    "generate_text"
]

def determine_intent(command):
    result = intent_model(command, intents)
    return result['labels'][0]

def generate_response(prompt):
    result = nlp_model(prompt, max_length=100, num_return_sequences=1,truncation=True)
    return result[0]['generated_text']
