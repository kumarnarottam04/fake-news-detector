"""
Evaluation & Explainability Configuration Data Class
"""
from dataclasses import dataclass

@dataclass
class EvaluationConfig:
    """Declarative Configuration for controlling Model Evaluation and XAI."""
    default_threshold: float = 0.50
    high_confidence_threshold: float = 90.0
    medium_confidence_threshold: float = 70.0
    top_explainability_words: int = 6
    save_plots: bool = True
    output_report_dir: str = "reports/evaluation"
