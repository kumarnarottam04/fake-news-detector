"""
Master Configurable Preprocessing Pipeline Coordinator
"""
import re
from typing import List, Union
from src.preprocessing.config import PreprocessingConfig
from src.preprocessing.normalizer import unicode_normalize, expand_contractions
from src.preprocessing.text_cleaner import cleaner

# Pre-compiled high-performance Regex objects
RE_HTML = re.compile(r'<[^>]+>')
RE_URL = re.compile(r'https?://\S+|www\.\S+')
RE_EMAIL = re.compile(r'\S+@\S+')
RE_NUMBERS = re.compile(r'[^a-zA-Z\s]')
RE_SPACES = re.compile(r'\s+')

class PreprocessingPipeline:
    """Configurable & Modular NLP Preprocessing Pipeline."""

    def __init__(self, config: PreprocessingConfig = None):
        self.config = config or PreprocessingConfig()

    def transform_text(self, text: str) -> str:
        """Executes full preprocessing pipeline according to configuration flags."""
        if not text or not isinstance(text, str):
            return ""

        # 1. Unicode Normalization
        if self.config.do_unicode_norm:
            text = unicode_normalize(text)

        # 2. Lowercasing
        if self.config.do_lowercasing:
            text = text.lower()

        # 3. HTML Stripping
        if self.config.strip_html:
            text = RE_HTML.sub(' ', text)

        # 4. URL Stripping / Token Replacement
        if self.config.strip_urls:
            repl = self.config.replace_url_token or ' '
            text = RE_URL.sub(repl, text)

        # 5. Email Stripping / Token Replacement
        if self.config.strip_emails:
            repl = self.config.replace_email_token or ' '
            text = RE_EMAIL.sub(repl, text)

        # 6. Contraction Expansion
        if self.config.expand_contractions:
            text = expand_contractions(text)

        # 7. Strip Special Symbols & Digits
        if self.config.strip_punctuation:
            text = RE_NUMBERS.sub(' ', text)

        # 8. Collapse Whitespace
        text = RE_SPACES.sub(' ', text).strip()

        # 9. Tokenization, Stopwords & Lemmatization via Cleaner Engine
        if self.config.remove_stopwords or self.config.do_lemmatization:
            text = cleaner.clean_text(text)

        return text

    def batch_transform(self, texts: List[str]) -> List[str]:
        """Transforms a batch of text strings."""
        return [self.transform_text(t) for t in texts]
