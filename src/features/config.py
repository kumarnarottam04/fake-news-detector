"""
Vectorizer Configuration Data Class
"""
from dataclasses import dataclass
from typing import Tuple, Optional, Union

@dataclass
class VectorizerConfig:
    """Declarative Configuration for controlling Feature Vectorizer hyperparameter execution."""
    max_features: int = 10000
    min_df: Union[int, float] = 2
    max_df: Union[int, float] = 0.95
    ngram_range: Tuple[int, int] = (1, 2)
    sublinear_tf: bool = True
    use_idf: bool = True
    smooth_idf: bool = True
    norm: str = 'l2'
    
    # Optional Feature Selection
    enable_feature_selection: bool = False
    k_selected_features: Optional[int] = 5000
