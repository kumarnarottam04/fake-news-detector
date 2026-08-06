import pytest
from src.preprocessing.text_cleaner import cleaner

def test_clean_text_lowercasing():
    input_text = "BREAKING NEWS ALERT"
    result = cleaner.clean_text(input_text)
    assert "breaking" in result
    assert "news" in result
    assert "alert" in result

def test_clean_text_html_and_url_removal():
    input_text = "<h1>Breaking!</h1> Visit http://example.com/test for more details."
    result = cleaner.clean_text(input_text)
    assert "h1" not in result
    assert "http" not in result
    assert "example" not in result
    assert "break" in result

def test_clean_text_stopword_removal():
    input_text = "This is a simple test of the stopword filter system"
    result = cleaner.clean_text(input_text)
    words = result.split()
    assert "this" not in words
    assert "is" not in words
    assert "the" not in words
    assert "test" in words or "simple" in words

def test_clean_text_empty_input():
    assert cleaner.clean_text("") == ""
    assert cleaner.clean_text(None) == ""
