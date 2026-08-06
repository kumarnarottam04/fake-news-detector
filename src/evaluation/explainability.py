"""
Explainable AI (XAI) Feature Importance Engine
"""
from typing import List, Dict, Any

def explain_prediction(tfidf_vector, vectorizer, model, top_n: int = 6) -> List[Dict[str, Any]]:
    """
    Calculates feature-level directional impact scores:
    Score(w_j) = TF-IDF(w_j, X_i) * beta_j
    
    Returns list of top positive (REAL supporting) and negative (FAKE supporting) keywords.
    """
    if not hasattr(model, 'coef_'):
        return []
        
    feature_names = vectorizer.get_feature_names_out()
    nonzero_indices = tfidf_vector.nonzero()[1]
    
    if len(nonzero_indices) == 0:
        return []
        
    coefficients = model.coef_[0]
    word_scores = []
    
    for idx in nonzero_indices:
        word = feature_names[idx]
        tfidf_val = tfidf_vector[0, idx]
        coef_val = coefficients[idx]
        impact_score = tfidf_val * coef_val
        
        supports = "REAL" if impact_score > 0 else "FAKE"
        word_scores.append({
            "word": word,
            "score": round(float(impact_score), 4),
            "supports": supports
        })
        
    # Sort by absolute impact score magnitude
    word_scores.sort(key=lambda x: abs(x['score']), reverse=True)
    return word_scores[:top_n]
