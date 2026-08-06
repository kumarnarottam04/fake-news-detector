"""
Confidence Estimation & Risk Assessment Module
"""

def estimate_confidence(prob_real: float, prob_fake: float) -> dict:
    """
    Calculates percentage confidence and maps to operational Risk Level.
    
    Risk Level Mapping:
    - HIGH CONFIDENCE: Confidence >= 90.0%
    - MEDIUM CONFIDENCE: 70.0% <= Confidence < 90.0%
    - LOW CONFIDENCE: Confidence < 70.0% (Flags for human verification)
    """
    prob_real = float(prob_real)
    prob_fake = float(prob_fake)
    
    max_prob = max(prob_real, prob_fake)
    confidence_pct = round(max_prob * 100, 2)
    
    if confidence_pct >= 90.0:
        risk_level = "HIGH_CONFIDENCE"
        recommendation = "Automated classification approved."
    elif confidence_pct >= 70.0:
        risk_level = "MEDIUM_CONFIDENCE"
        recommendation = "Standard classification approved."
    else:
        risk_level = "LOW_CONFIDENCE"
        recommendation = "Low confidence prediction; recommended for human fact-checker review."
        
    return {
        "confidence_percentage": confidence_pct,
        "risk_level": risk_level,
        "recommendation": recommendation
    }
