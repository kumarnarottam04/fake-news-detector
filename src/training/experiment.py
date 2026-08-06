"""
Experiment Tracking & Metadata Audit System
"""
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from src.utils.logger import logger

class ExperimentTracker:
    """Logs and tracks training experiment runs to JSON metadata files."""

    def __init__(self, log_dir: str = "models/metadata"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log_experiment(self, model_name: str, params: dict, metrics: dict, training_duration: float) -> str:
        """Records an experiment run audit log."""
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        exp_id = f"exp_{timestamp_str}_{model_name}"

        experiment_payload = {
            "experiment_id": exp_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model_name": model_name,
            "hyperparameters": params,
            "metrics": metrics,
            "performance": {
                "training_duration_seconds": round(training_duration, 4)
            }
        }

        output_path = self.log_dir / f"{exp_id}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(experiment_payload, f, indent=2)

        logger.info(f"Experiment log saved to: {output_path}")
        return exp_id
