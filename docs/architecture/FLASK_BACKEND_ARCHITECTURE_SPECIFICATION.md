# Master Flask Backend Architecture & REST API Specification

**Project Title:** Fake News Detection System  
**Document Type:** Production Flask Backend Architecture & REST API Specification  
**Author:** Principal Backend Architect & API Lead  
**Target Environment:** Python 3.12+, Flask 3.0+, Gunicorn 22.0+, Flask-CORS, Flask-Limiter  

---

## 1. Executive Summary & Design Patterns

The **Flask Backend Layer** acts as the high-performance controller interface connecting client browsers to the underlying NLP Preprocessing Engine, TF-IDF Feature Builder, and Scikit-learn Classifier.

### Key Architecture Patterns
1. **Application Factory Pattern (`create_app`):** Encapsulates application creation inside a factory function, enabling clean environment switching (`DevelopmentConfig`, `ProductionConfig`, `TestingConfig`) and isolated test client instantiation (`pytest`).
2. **Flask Blueprint Architecture:** Organizes API routes into decoupled Blueprints (`api_bp = Blueprint('api', __name__)`), preventing single-file route sprawl.
3. **Service Layer Pattern (`PredictionService`):** Controllers handle HTTP validation and response serialization, delegating business logic to business services.
4. **Thread-Safe Singleton Model Loader (`ModelLoader`):** Lazy-loads `.joblib` model and vectorizer binary artifacts into memory **once**, eliminating per-request disk I/O overhead.
5. **Centralized Exception Dispatcher (`@app.errorhandler`):** Catches custom domain errors (`ValidationError`, `ModelLoadError`, `PredictionError`) and maps them to standardized JSON error payloads with appropriate HTTP status codes.

---

## 2. Complete REST API Endpoints Specification

```
+-----------------------------------------------------------------------------------+
|                            FLASK REST API ROUTE MAP                               |
+-----------+-------------------+---------------------------------------------------+
| Method    | Endpoint Path     | Purpose & Description                             |
+-----------+-------------------+---------------------------------------------------+
| GET       | /                 | Renders SPA HTML View (templates/index.html)      |
| GET       | /health           | System health check, uptime, RAM & model status   |
| POST      | /api/predict      | Real-time article text classification & XAI words |
| GET       | /api/samples      | Fetches preset real and fake articles for UI test  |
| GET       | /api/model-info   | Model metadata, versioning, feature dimension     |
| GET       | /api/metrics      | Validation benchmark evaluation metrics summary   |
+-----------+-------------------+---------------------------------------------------+
```

---

## 3. End-to-End API Execution Sequence Diagram

```
[ CLIENT BROWSER / REST CLIENT ]
              |
              | 1. HTTP POST /api/predict { "text": "Raw news text..." }
              v
[ FLASK WSGI SERVER (Gunicorn / App Factory) ]
              |
              | 2. Rate Limiter (30 req/min limit check) & Max Payload Check (1MB)
              v
[ API CONTROLLER (src/api/routes.py) ]
              |
              | 3. Validate Request Payload (JSON schema, non-empty, len >= 50)
              v
[ PREDICTION SERVICE (src/services/prediction_service.py) ]
              |
              +----------------------------+----------------------------+
              |                                                         |
              v                                                         v
[ PREPROCESSING ENGINE ]                                  [ SINGLETON MODEL LOADER ]
  - Lowercasing                                             - Warm joblib model in RAM
  - Regex HTML/URL removal                                  - Warm TF-IDF vectorizer
  - NLTK Stopwords & Lemmatization                                      |
              |                                                         |
              +----------------------------+----------------------------+
                                           |
                                           v
[ TF-IDF TRANSFORMER & MODEL INFERENCE ]
  - Compute Feature Matrix (1 x 10,000)
  - Compute P(REAL) and P(FAKE) probabilities
  - Extract Top Feature Coefficients (\beta_j * x_{i,j})
                                           |
                                           v
[ FLASK RESPONSE BUILDER ]
  - Serialize to standardized JSON schema
  - Return HTTP 200 OK + Security Headers (nosniff, DENY)
                                           |
              +----------------------------+
              |
              v
[ CLIENT BROWSER / REST CLIENT ]
  - Render prediction badge, confidence meter, and word impact badges
```

---

## 4. Standardized JSON API Response Schemas

### 1. Success Prediction Response (`POST /api/predict` - HTTP 200 OK)

```json
{
  "success": true,
  "prediction": {
    "label": "REAL",
    "class_id": 1,
    "confidence": 96.45,
    "probabilities": {
      "fake": 0.0355,
      "real": 0.9645
    }
  },
  "explanation": {
    "top_indicative_words": [
      {"word": "official", "score": 1.421, "supports": "REAL"},
      {"word": "report", "score": 1.152, "supports": "REAL"},
      {"word": "claim", "score": -0.845, "supports": "FAKE"}
    ]
  },
  "meta": {
    "latency_ms": 38.42,
    "timestamp": "2026-08-05T12:23:53Z",
    "model_version": "1.0.0"
  }
}
```

### 2. Standardized Error Response (HTTP 400 / 429 / 500 / 503)

```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Article text must be at least 50 characters long.",
    "status_code": 400
  },
  "timestamp": "2026-08-05T12:23:53Z"
}
```

### 3. System Health Check Response (`GET /health` - HTTP 200 OK)

```json
{
  "status": "healthy",
  "model_loaded": true,
  "vectorizer_loaded": true,
  "uptime_seconds": 14205.8,
  "memory_usage_mb": 142.5,
  "version": "1.0.0"
}
```

---

## 5. Security & Performance Controls

1. **Max Payload Cap:** `MAX_CONTENT_LENGTH = 1 * 1024 * 1024` (1 MB limit) enforced at Flask WSGI level to prevent memory exhaustion DoS attacks.
2. **Rate Limiting:** IP-based rate limiting via `Flask-Limiter` restricting endpoints to **30 requests per minute** on `/api/predict`.
3. **CORS Restrictions:** Configured via `Flask-CORS` enabling origin filtering.
4. **Header Hardening:** Every API response attaches security headers:
   - `X-Content-Type-Options: nosniff`
   - `X-Frame-Options: DENY`
   - `X-XSS-Protection: 1; mode=block`
5. **Input Sanitization:** Strips HTML/XML tags and script symbols via regex prior to model inference.

---

## 6. Centralized Error Dispatcher Map

```
                  +-----------------------------------+
                  |      Incoming HTTP Request        |
                  +-----------------------------------+
                                    |
                                    v
                  +-----------------------------------+
                  |   Flask Route Exception Handler   |
                  +-----------------------------------+
                                    |
      +-----------------------------+-----------------------------+
      |                             |                             |
      v                             v                             v
+---------------------------+ +---------------------------+ +---------------------------+
| ValidationError           | | ModelLoadError            | | RateLimitExceeded (429)   |
| -> Return HTTP 400 Bad    | | -> Return HTTP 503       | | -> Return HTTP 429       |
|    Request JSON payload   | |    Service Unavailable    | |    Too Many Requests    |
+---------------------------+ +---------------------------+ +---------------------------+
```

---

## 7. Package Directory Architecture (`src/api/` & `backend/`)

```
backend/
├── app.py                          # Application Factory entry point
├── config.py                       # Configuration classes (Dev/Prod/Test)
├── Procfile                        # Gunicorn startup configuration for cloud
├── render.yaml                     # Render Infrastructure-as-Code blueprint
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py               # REST API Blueprint routes
│   │   ├── schemas.py              # Request/Response JSON validation schemas
│   │   └── middleware.py           # CORS, rate limiting, and security headers
│   └── services/
│       ├── __init__.py
│       ├── prediction_service.py   # Business logic orchestrator
│       └── health_service.py       # System health monitor
└── tests/
    └── integration/
        └── test_api.py             # Pytest API integration test client
```
