import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix, roc_auc_score, roc_curve
)
from pathlib import Path
from src.utils.logger import logger

def evaluate_model(model, X_test, y_test, class_names=['FAKE', 'REAL'], output_dir: Path = None) -> dict:
    """
    Evaluates ML classifier performance metrics and logs classification reports.
    """
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1] if hasattr(model, 'predict_proba') else None
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, zero_division=0)
    rec = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    
    auc = roc_auc_score(y_test, y_proba) if y_proba is not None else 0.0
    
    logger.info("=== MODEL EVALUATION METRICS ===")
    logger.info(f"Accuracy : {acc * 100:.2f}%")
    logger.info(f"Precision: {prec * 100:.2f}%")
    logger.info(f"Recall   : {rec * 100:.2f}%")
    logger.info(f"F1 Score : {f1 * 100:.2f}%")
    logger.info(f"ROC AUC  : {auc:.4f}")
    
    report = classification_report(y_test, y_pred, target_names=class_names)
    logger.info(f"\nClassification Report:\n{report}")
    
    cm = confusion_matrix(y_test, y_pred)
    
    metrics_summary = {
        "accuracy": float(acc),
        "precision": float(prec),
        "recall": float(rec),
        "f1_score": float(f1),
        "roc_auc": float(auc),
        "confusion_matrix": cm.tolist()
    }
    
    return metrics_summary
