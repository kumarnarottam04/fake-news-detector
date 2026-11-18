import time
import numpy as np
from src.preprocessing.text_cleaner import cleaner
from src.prediction.model_loader import ModelLoader
from src.utils.logger import logger

def predict_article(raw_text: str) -> dict:
    """
    Executes end-to-end prediction pipeline for a given news article.
    
    Returns structured dictionary containing:
    - label: "REAL" or "FAKE"
    - class_id: 1 (REAL) or 0 (FAKE)
    - confidence: float percentage (e.g. 96.45)
    - probabilities: dict of class probabilities
    - top_words: list of influential feature words with directional scores
    - latency_ms: processing duration in milliseconds
    """
    start_time = time.time()
    
    if not raw_text or len(raw_text.strip()) < 50:
        raise ValueError("Article text must be at least 50 characters long.")
        
    loader = ModelLoader()
    if not loader.is_loaded:
        loaded = loader.load_artifacts()
        if not loaded:
            raise RuntimeError("ML model artifacts are not initialized. Please train the model first.")
            
    model = loader.model
    vectorizer = loader.vectorizer
    
    # 1. Clean input text
    clean_text = cleaner.clean_text(raw_text)
    if not clean_text:
        raise ValueError("Text contains no valid words after preprocessing.")
        
    # 2. Transform text to TF-IDF feature matrix
    tfidf_vector = vectorizer.transform([clean_text])
    
    # 3. Model Inference & Probabilities
    prediction_id = int(model.predict(tfidf_vector)[0])
    
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(tfidf_vector)[0]
        prob_fake = float(probabilities[0])
        prob_real = float(probabilities[1])
    elif hasattr(model, 'decision_function'):
        decision = float(model.decision_function(tfidf_vector)[0])
        # Convert decision function score to calibrated probability via Sigmoid
        prob_real = float(1.0 / (1.0 + np.exp(-np.clip(decision, -20, 20))))
        prob_fake = float(1.0 - prob_real)
    else:
        prob_real = 1.0 if prediction_id == 1 else 0.0
        prob_fake = 1.0 - prob_real
    
    label = "REAL" if prediction_id == 1 else "FAKE"
    confidence = prob_real if prediction_id == 1 else prob_fake
    confidence_pct = round(confidence * 100, 2)
    
    # 4. Feature Weight Explainability Calculation
    top_words = extract_feature_importance(tfidf_vector, vectorizer, model, top_n=6)
    
    latency_ms = round((time.time() - start_time) * 1000, 2)
    
    logger.info(f"Prediction generated: label={label}, confidence={confidence_pct}%, latency={latency_ms}ms")
    
    return {
        "success": True,
        "prediction": {
            "label": label,
            "class_id": prediction_id,
            "confidence": confidence_pct,
            "probabilities": {
                "fake": round(prob_fake, 4),
                "real": round(prob_real, 4)
            }
        },
        "explanation": {
            "top_indicative_words": top_words
        },
        "meta": {
            "latency_ms": latency_ms
        }
    }

def extract_feature_importance(tfidf_vector, vectorizer, model, top_n=6) -> list:
    """Extracts words present in the document that contributed most to the prediction decision."""
    feature_names = vectorizer.get_feature_names_out()
    nonzero_indices = tfidf_vector.nonzero()[1]
    
    if len(nonzero_indices) == 0:
        return []
        
    # Handle linear models with coef_ (e.g. Logistic Regression / SVM)
    if hasattr(model, 'coef_'):
        coefficients = model.coef_[0]
        word_scores = []
        
        for idx in nonzero_indices:
            word = feature_names[idx]
            tfidf_weight = tfidf_vector[0, idx]
            coef_weight = coefficients[idx]
            impact_score = tfidf_weight * coef_weight
            
            supports_class = "REAL" if impact_score > 0 else "FAKE"
            word_scores.append({
                "word": word,
                "score": round(float(impact_score), 4),
                "supports": supports_class
            })
            
        # Sort by absolute impact magnitude
        word_scores.sort(key=lambda x: abs(x['score']), reverse=True)
        return word_scores[:top_n]
    else:
        # Fallback for non-linear tree models
        return []
