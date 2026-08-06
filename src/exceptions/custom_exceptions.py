"""
Domain Exception Taxonomy
"""

class FakeNewsDetectorException(Exception):
    """Base exception for all Fake News Detection system errors."""
    def __init__(self, message: str = "An unexpected domain error occurred."):
        super().__init__(message)
        self.message = message

class ValidationError(FakeNewsDetectorException):
    """Raised when input text or payload fails validation checks."""
    pass

class ModelLoadError(FakeNewsDetectorException):
    """Raised when serialized model or vectorizer artifacts cannot be loaded."""
    pass

class PredictionError(FakeNewsDetectorException):
    """Raised when model inference or feature calculation fails."""
    pass

class ConfigurationError(FakeNewsDetectorException):
    """Raised when application environment settings or path configurations are invalid."""
    pass

class DataError(FakeNewsDetectorException):
    """Raised when dataset files are corrupted, missing, or malformed."""
    pass
