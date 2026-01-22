import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Download necessary NLTK data
def download_nltk_resources():
    resources = ['punkt', 'wordnet', 'punkt_tab']
    for resource in resources:
        try:
            nltk.data.find(f'tokenizers/{resource}')
        except LookupError:
            try:
                nltk.data.find(f'corpora/{resource}')
            except LookupError:
                print(f"Downloading NLTK resource: {resource}")
                nltk.download(resource, quiet=True)

download_nltk_resources()

lemmatizer = WordNetLemmatizer()

def preprocess_text(text):
    """
    Tokenizes and lemmatizes the input text.
    Args:
        text (str): Input text string.
    Returns:
        list: List of processed tokens.
    """
    if not text:
        return []
    
    try:
        # Tokenize
        tokens = word_tokenize(text.lower())
        # Lemmatize and remove non-alphanumeric characters
        processed_tokens = [lemmatizer.lemmatize(token) for token in tokens if token.isalnum()]
        return processed_tokens
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        return []
