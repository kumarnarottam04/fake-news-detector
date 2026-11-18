import re
import string
from pathlib import Path
import nltk

# Ensure workspace nltk_data directory is registered
_WORKSPACE_ROOT = Path(__file__).resolve().parent.parent.parent
_LOCAL_NLTK_DATA = _WORKSPACE_ROOT / 'data' / 'nltk_data'
if _LOCAL_NLTK_DATA.exists() and str(_LOCAL_NLTK_DATA) not in nltk.data.path:
    nltk.data.path.insert(0, str(_LOCAL_NLTK_DATA))

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from src.utils.logger import logger

class TextCleaner:
    """Natural Language Processing Text Preprocessing Engine."""
    
    def __init__(self):
        self._ensure_nltk_resources()
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()
        
    def _ensure_nltk_resources(self):
        """Downloads required NLTK corpuses if missing."""
        resources = ['stopwords', 'wordnet']
        for res in resources:
            try:
                nltk.data.find(f'corpora/{res}')
            except LookupError:
                logger.info(f"Downloading NLTK resource: {res}")
                nltk.download(res, quiet=True)

    def clean_text(self, text: str) -> str:
        """
        Executes standard NLP cleaning sequence:
        1. Lowercasing
        2. HTML & URL removal
        3. Punctuation & Digit stripping
        4. Tokenization & Stopword removal
        5. WordNet Lemmatization
        """
        if not text or not isinstance(text, str):
            return ""
            
        # 1. Lowercasing
        text = text.lower()
        
        # 2. HTML Tag Stripping
        text = re.sub(r'<[^>]+>', ' ', text)
        
        # 3. URL Stripping
        text = re.sub(r'https?://\S+|www\.\S+', ' ', text)
        
        # 4. Remove Email Addresses
        text = re.sub(r'\S+@\S+', ' ', text)
        
        # 5. Remove Punctuation & Numbers
        text = re.sub(r'[^a-z\s]', ' ', text)
        
        # 6. Tokenize by Whitespace
        tokens = text.split()
        
        # 7. Stopword Filtering & Lemmatization
        cleaned_tokens = [
            self.lemmatizer.lemmatize(token)
            for token in tokens
            if token not in self.stop_words and len(token) > 2
        ]
        
        return " ".join(cleaned_tokens)

# Global default instance
cleaner = TextCleaner()
