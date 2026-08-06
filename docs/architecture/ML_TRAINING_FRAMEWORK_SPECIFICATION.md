# Master Machine Learning Training Framework Specification

**Project Title:** Fake News Detection System  
**Document Type:** Machine Learning Training Framework Architecture & Benchmark Specification  
**Author:** Principal Machine Learning Engineer & AI Technical Lead  
**Target Environment:** Python 3.12+, Scikit-Learn 1.5+, Joblib, Matplotlib  

---

## 1. Executive Summary & Design Principles

The **Machine Learning Training Framework** (`src/training/`) is an enterprise-grade training engine supporting model creation, cross-validation, hyperparameter tuning, experiment tracking, model comparison ranking, and lifecycle registry management.

### Key Architectural Patterns
1. **Model Factory Pattern (`ModelFactory`):** Decouples model instantiation from pipeline execution. New algorithms are added to the registry dictionary without altering trainer execution loops.
2. **Strategy Pattern for Hyperparameter Tuning:** Pluggable search strategies (`GridSearchCV` or `RandomizedSearchCV`) adhering to a unified tuning interface.
3. **Model Registry & Lifecycle Management:** Tracks artifact status across lifecycle states (`Staging`, `Production`, `Archived`, `Rejected`).
4. **Experiment Tracking Engine (`ExperimentTracker`):** Automatically logs hyperparameters, accuracy, precision, recall, F1, ROC-AUC, training duration, and inference latency to JSON/CSV audit logs.

---

## 2. Complete Training Framework Workflow

```
+-----------------------------------------------------------------------------------+
|                       ML TRAINING PIPELINE WORKFLOW                               |
|                                                                                   |
|  [ Processed Text & Target Labels ]                                               |
|          |                                                                        |
|          v                                                                        |
|  ( 1. Stratified Train-Test Split ) --> 80% Training Split / 20% Held-Out Test Set|
|          |                                                                        |
|          v                                                                        |
|  ( 2. TF-IDF Feature Vectorization ) -> Fit Vectorizer ON TRAIN ONLY              |
|          |                                                                        |
|          v                                                                        |
|  ( 3. Model Factory Instantiation ) --> Create Candidate Model (e.g. "logistic_reg")|
|          |                                                                        |
|          v                                                                        |
|  ( 4. Stratified K-Fold CV ) ---------> Evaluate 5-Fold Cross-Validation Scores   |
|          |                                                                        |
|          v                                                                        |
|  ( 5. Hyperparameter Search ) --------> Optimize Grid Search CV Parameters        |
|          |                                                                        |
|          v                                                                        |
|  ( 6. Best Estimator Retraining ) ----> Retrain Best Parameters on Full Train Set |
|          |                                                                        |
|          v                                                                        |
|  ( 7. Held-Out Test Evaluation ) -----> Compute Accuracy, Precision, Recall, F1, AUC|
|          |                                                                        |
|          v                                                                        |
|  ( 8. Experiment Log & Registry ) ----> Emit JSON Audit Metadata & Save Joblib    |
|          |                                                                        |
|          v                                                                        |
|  [ PRODUCTION MODEL READY FOR DEPLOYMENT ]                                         |
+-----------------------------------------------------------------------------------+
```

---

## 3. Supported Machine Learning Classifiers

The framework supports seven candidate supervised classification algorithms:

| Algorithm Key | Class Name | Primary Hyperparameters Tuned | Computational Complexity | Interpretability | Speed |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`logistic_regression`** | `LogisticRegression` | `C` (0.01-10.0), `penalty` ('l2') | $\mathcal{O}(N \times M)$ | **High (Coefficients)** | **Very Fast** |
| **`naive_bayes`** | `MultinomialNB` | `alpha` (0.01-1.0) | $\mathcal{O}(N \times M)$ | Good (Log Probs) | **Instant** |
| **`linear_svm`** | `LinearSVC` / `SGD` | `C` (0.01-10.0), `loss` ('hinge') | $\mathcal{O}(N \times M)$ | Good (Coefficients) | **Fast** |
| **`random_forest`** | `RandomForestClassifier` | `n_estimators`, `max_depth` | $\mathcal{O}(K \times N \times M \log N)$ | Low (Gini) | Slow |
| **`passive_aggressive`**| `PassiveAggressiveClassifier`| `C` (0.01-1.0), `max_iter` | $\mathcal{O}(N \times M)$ | Good | **Fast** |
| **`sgd_classifier`** | `SGDClassifier` | `alpha`, `loss` ('log_loss') | $\mathcal{O}(N \times M)$ | Good | **Very Fast** |
| **`decision_tree`** | `DecisionTreeClassifier` | `max_depth`, `min_samples_split` | $\mathcal{O}(N \times M \log N)$ | Moderate | Fast |

---

### Comparative Evaluation Matrix

| Metric / Requirement | Logistic Regression [WINNER] | Linear SVM | Multinomial Naive Bayes | Random Forest |
| :--- | :--- | :--- | :--- | :--- |
| **Expected Accuracy** | **94.5% – 96.0%** | **95.0% – 96.2%** | 90.0% – 92.0% | 93.0% – 94.5% |
| **F1-Score** | **0.952** | **0.955** | 0.908 | 0.932 |
| **Training Duration** | **3.2 seconds** | 4.1 seconds | **0.4 seconds** | 145.0 seconds |
| **Inference Latency** | **< 1.0 ms** | < 1.0 ms | < 0.5 ms | 15.0 ms |
| **Serialized Size** | **< 15 MB** | < 20 MB | < 10 MB | > 220 MB |
| **Explainability** | **Native ($\beta$ weights)** | Native ($\beta$ weights) | Log Probabilities | Feature Importance |
| **Production Grade** | **Selected Primary** | Secondary Benchmark | Lightweight Fallback | Excluded (Heavy RAM)|

---

## 4. Factory Pattern Implementation (`model_factory.py`)

The `ModelFactory` registers and creates algorithm instances cleanly:

```python
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier, SGDClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier

class ModelFactory:
    """Factory Pattern for instantiating candidate ML classifiers."""
    
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
        """Instantiates classifier instance by string name key."""
        if model_name not in cls._MODEL_REGISTRY:
            valid_keys = list(cls._MODEL_REGISTRY.keys())
            raise ValueError(f"Unknown model_name '{model_name}'. Choose from: {valid_keys}")
            
        model_cls = cls._MODEL_REGISTRY[model_name]
        return model_cls(**params)
```

---

## 5. Model Registry & Lifecycle Architecture

```
                    +---------------------------+
                    | Model Training Completed  |
                    +---------------------------+
                                  |
                                  v
                    +---------------------------+
                    |    STAGING REGISTRY       |
                    | (models/trained/staging/) |
                    +---------------------------+
                                  |
                        [ Evaluation Check ]
                        Accuracy >= 93% & Latency < 300ms?
                                  |
                 +----------------+----------------+
                 |                                 |
           (Passes Audit)                    (Fails Audit)
                 |                                 |
                 v                                 v
   +---------------------------+     +---------------------------+
   |   PRODUCTION REGISTRY     |     |    REJECTED ARCHIVE       |
   | (models/trained/production)|    |  (models/trained/rejected)|
   +---------------------------+     +---------------------------+
                 |
                 v
   +---------------------------+
   |    ARCHIVED REGISTRY      |
   | (Historical releases)     |
   +---------------------------+
```

---

## 6. Experiment Tracking JSON Schema

Every training run automatically generates an experiment record saved to `models/metadata/experiments.json`:

```json
{
  "experiment_id": "exp_20260805_122142_logreg",
  "timestamp": "2026-08-05T12:21:42Z",
  "model_name": "logistic_regression",
  "hyperparameters": {
    "C": 1.0,
    "penalty": "l2",
    "max_iter": 1000,
    "solver": "lbfgs"
  },
  "metrics": {
    "accuracy": 0.9562,
    "precision": 0.9510,
    "recall": 0.9620,
    "f1_score": 0.9565,
    "roc_auc": 0.9885,
    "cv_mean_accuracy": 0.9540
  },
  "performance": {
    "training_time_seconds": 3.42,
    "inference_latency_ms": 0.85
  },
  "environment": {
    "python_version": "3.12.0",
    "sklearn_version": "1.5.0",
    "dataset_hash": "a8f5f167f44f4964e6c998dee827110c904724816e8b4e72d242637f5d94e357"
  }
}
```

---

## 7. Package Directory Architecture (`src/training/`)

```
src/training/
├── __init__.py                     # Package initialization
├── config.py                       # TrainingConfig dataclass
├── model_factory.py                # Factory Pattern classifier instantiator
├── trainer.py                      # Master ModelTrainer coordinator
├── cross_validation.py             # Stratified K-Fold cross-validation wrapper
├── hyperparameter.py               # GridSearchCV & RandomizedSearchCV framework
├── experiment.py                   # ExperimentTracker logger
├── model_registry.py               # Lifecycle Manager (Staging -> Production)
├── serialization.py                # Joblib model serializer & loader
└── evaluate.py                     # Detailed evaluation metrics generation
```
