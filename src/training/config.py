"""
Training Pipeline Configuration Data Class
"""
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

@dataclass
class TrainingConfig:
    """Declarative Configuration for Machine Learning Training Pipelines."""
    model_name: str = "logistic_regression"
    test_size: float = 0.2
    random_state: int = 42
    stratify: bool = True
    
    # Cross Validation
    cv_folds: int = 5
    
    # Hyperparameter Tuning
    enable_tuning: bool = False
    tuning_strategy: str = "grid"  # 'grid' or 'random'
    param_grid: Optional[Dict[str, Any]] = field(default_factory=dict)
    
    # Output Paths
    output_model_path: str = "models/model.joblib"
    output_vectorizer_path: str = "models/tfidf_vectorizer.joblib"
