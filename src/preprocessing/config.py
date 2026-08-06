"""
Preprocessing Configuration Data Class & Feature Flags
"""
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class PreprocessingConfig:
    """Declarative Configuration for controlling NLP Pipeline execution."""
    do_lowercasing: bool = True
    do_unicode_norm: bool = True
    strip_html: bool = True
    strip_urls: bool = True
    strip_emails: bool = True
    strip_numbers: bool = True
    strip_punctuation: bool = True
    expand_contractions: bool = True
    remove_stopwords: bool = True
    do_lemmatization: bool = True
    do_stemming: bool = False
    
    min_word_length: int = 2
    max_word_length: int = 40
    min_article_chars: int = 50
    
    custom_stopwords: Optional[List[str]] = field(default_factory=list)
    replace_url_token: Optional[str] = None
    replace_email_token: Optional[str] = None
