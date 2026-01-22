import json
import os
from nlp.preprocessing import preprocess_text

class IntentClassifier:
    def __init__(self, intents_file='data/intents.json'):
        self.intents = []
        # Construct absolute path to ensure file is found
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, intents_file)
        self.load_intents()

    def load_intents(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r') as f:
                    data = json.load(f)
                    self.intents = data['intents']
            else:
                print(f"Intents file not found at: {self.file_path}")
        except Exception as e:
            print(f"Error loading intents: {e}")

    def predict(self, text):
        """
        Predicts the intent of the given text using rule-based matching.
        Args:
            text (str): Input text.
        Returns:
            dict: The matched intent object or None.
        """
        if not text:
            return None
            
        text = text.lower()
        processed_input = set(preprocess_text(text))
        
        best_intent = None
        max_score = 0

        for intent in self.intents:
            for pattern in intent['patterns']:
                # 1. Exact phrase match (Highest priority)
                if pattern in text:
                    return intent
                
                # 2. Token overlap match
                processed_pattern = set(preprocess_text(pattern))
                if not processed_pattern:
                    continue
                    
                intersection = processed_input.intersection(processed_pattern)
                score = len(intersection) / len(processed_pattern) # Jaccard-ish index based on pattern coverage
                
                if score > max_score:
                    max_score = score
                    best_intent = intent

        # Threshold can be adjusted
        if max_score >= 0.5:
            return best_intent
            
        return None

    def get_response(self, intent_tag):
        """
        Returns a random response for a given intent tag.
        """
        import random
        for intent in self.intents:
            if intent['tag'] == intent_tag:
                responses = intent.get('responses', [])
                if responses:
                    return random.choice(responses)
        return None
