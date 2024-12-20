from transformers import pipeline

# Load NLP model
nlp_model = pipeline("text-generation", model="EleutherAI/gpt-neo-125M")

def generate_response(prompt):
    result = nlp_model(prompt, max_length=100, num_return_sequences=1,truncation=True)
    return result[0]['generated_text']
