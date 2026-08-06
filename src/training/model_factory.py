"""
Model Factory Pattern Implementation
"""
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

class ModelFactory:
    """Factory Pattern class for instantiating machine learning classifiers."""

    _MODEL_REGISTRY = {
        'logistic_regression': LogisticRegression,
        'naive_bayes': MultinomialNB,
        'linear_svm': LinearSVC,
        'random_forest': RandomForestClassifier,
        'passive_aggressive': PassiveAggressiveClassifier,
        'sgd_classifier': SGDClassifier,
        'decision_tree': DecisionTreeClassifier
    }

    @classmethod
    def create_model(cls, model_name: str, **params):
        """Instantiates classifier object by string key."""
        model_key = model_name.lower()
        if model_key not in cls._MODEL_REGISTRY:
            valid_keys = list(cls._MODEL_REGISTRY.keys())
            raise ValueError(f"Unknown model_name '{model_name}'. Select from: {valid_keys}")

        model_cls = cls._MODEL_REGISTRY[model_key]
        return model_cls(**params)

    @classmethod
    def list_supported_models(cls):
        """Returns list of all supported algorithm keys."""
        return list(cls._MODEL_REGISTRY.keys())
