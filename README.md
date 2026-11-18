# Fake News Analysis System using ML & NLP

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.3-green.svg)](https://flask.palletsprojects.com/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.5.0-orange.svg)](https://scikit-learn.org/)
[![NLTK](https://img.shields.io/badge/NLTK-3.8.1-yellow.svg)](https://www.nltk.org/)
[![Deploy](https://img.shields.io/badge/Render-Production-purple.svg)](https://render.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, machine-learning-powered web application designed to predict whether a news article is **REAL** or **FAKE** in real-time. Built as a 120-hour Artificial Intelligence Internship Project, this platform combines Natural Language Processing (NLP), TF-IDF feature engineering, Logistic Regression classification, and word-level feature Explainable AI (XAI) in a responsive glassmorphism web UI.

---

## 🌟 Key Features

- **Sub-Second Real-Time Inference:** Predicts article authenticity with $<300\text{ms}$ latency.
- **Probabilistic Confidence Meter:** Calculates class probability distributions ($P(\text{REAL})$ vs $P(\text{FAKE})$) and risk levels.
- **Linguistic Word-Level Explainability (XAI):** Extracts top TF-IDF feature weights ($\beta_j \times x_{i,j}$) driving the model's decision.
- **Clean Architecture:** Strict separation between Presentation (HTML/CSS/JS), REST API Controllers (Flask), NLP Preprocessing Engine, ML Training Modules, and Data Storage.
- **Thread-Safe Model Warm Loading:** Utilizes Singleton design pattern (`ModelLoader`) to prevent disk I/O bottlenecks.
- **Responsive Dark/Light Mode UI:** Built with Glassmorphism CSS styling, micro-animations, and dynamic DOM updates.
- **Production Ready:** Configured for stateless cloud deployment on Render with Gunicorn WSGI and automated NLTK resource bootstrap.

---

## 🏗️ System Architecture

```
+-----------------------------------------------------------------------------------+
|                               SYSTEM ARCHITECTURE                                 |
|                                                                                   |
|  [ Presentation Layer ] (HTML5 / Vanilla CSS3 / Modern Glassmorphism JS)          |
|            │                                                                      |
|            │ HTTP REST POST /api/predict                                          |
|            ▼                                                                      |
|  [ Controller Layer ] (Flask WSGI Server + Rate Limiter + Security Headers)       |
|            │                                                                      |
|            │ Validate Payload & Dispatch                                          |
|            ▼                                                                      |
|  [ NLP Engine ] (NLTK Tokenizer + Stopword Filter + WordNet Lemmatization)       |
|            │                                                                      |
|            │ Clean Token String                                                   |
|            ▼                                                                      |
|  [ ML Inference Engine ] (TF-IDF Vectorizer + Logistic Regression Classifier)     |
|            │                                                                      |
|            │ P(REAL), P(FAKE) & Feature Coefficient Intersection \beta_j * x_{i,j}|
|            ▼                                                                      |
|  [ XAI Explanation Builder ] (Computes Top Indicative Keyword Weights)           |
|            │                                                                      |
|            │ JSON Response Payload                                                |
|            ▼                                                                      |
|  [ Client UI Update ] (Animates Gauge, Renders REAL/FAKE Badge & Word Badges)     |
+-----------------------------------------------------------------------------------+
```

---

## 📁 Repository Structure

```
fake_news_detection/
├── artifacts/                      # Archived models, plots & metrics
├── config/                         # System-wide paths, constants & logging settings
├── data/                           # Raw, interim, and processed CSV datasets
├── docs/                           # System architecture & setup documentation
│   ├── architecture/               # SRS, Data, Preprocessing, ML & API specifications
│   ├── deployment/                 # Cloud deployment & DevOps specifications
│   └── PORTFOLIO_DOCUMENTATION_AND_VIVA_GUIDE.md  # Viva 100 Q&A & resume entries
├── logs/                           # Application, error, and prediction logs
├── models/                         # Active runtime models and metadata (.joblib)
├── notebooks/                      # Sequenced Jupyter research notebooks
├── scripts/                        # Operational CLI automation scripts
├── src/                            # Clean Architecture Application Packages
│   ├── api/                        # REST API routes and controllers
│   ├── exceptions/                 # Custom domain exceptions
│   ├── features/                   # TF-IDF feature builder & feature selector
│   ├── preprocessing/              # NLP text cleaner, normalizer & pipeline
│   ├── prediction/                 # Singleton model loader & predictor
│   ├── training/                   # Model trainer & ModelFactory
│   ├── evaluation/                 # Metrics calculator & XAI explainability engine
│   └── utils/                      # Logging & safe serialization helpers
├── static/                         # Responsive CSS3 glassmorphism & JS assets
├── templates/                      # Semantic HTML5 view template (index.html)
├── tests/                          # Automated Pytest suite (Unit & Integration)
├── app.py                          # Flask WSGI Server entry point (Factory Pattern)
├── Procfile                        # Gunicorn WSGI startup configuration
├── render.yaml                     # Render Infrastructure-as-Code blueprint
├── pyproject.toml                  # Black, isort, and Pytest configuration
├── requirements.txt                # Pinned dependencies
├── runtime.txt                     # Python 3.12.0 lock
└── README.md                       # Master project overview
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.12 or higher.
- Git installed.

### 2. Local Installation

```bash
# 1. Clone repository
git clone https://github.com/your-username/fake-news-detection-system.git
cd fake-news-detection-system

# 2. Create and activate virtual environment
python -m venv venv
# Windows (PowerShell):
.\venv\Scripts\Activate.ps1
# macOS / Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Train initial Machine Learning Model
python -m src.training.train

# 5. Launch Flask Server
python app.py
```
Open your browser at `http://localhost:5000`.

---

## 🧪 Automated Testing

Run the full pytest suite (Unit + Integration tests):

```bash
pytest tests/ -v
```

---

## 📊 Model Performance Metrics

| Metric | Target Metric | Achieved Benchmark |
| :--- | :--- | :--- |
| **Accuracy** | $\ge 93.0\%$ | **95.6%** |
| **Precision (Real)** | $\ge 92.0\%$ | **95.1%** |
| **Recall (Real)** | $\ge 92.0\%$ | **96.2%** |
| **F1-Score** | $\ge 0.920$ | **0.956** |
| **ROC-AUC** | $\ge 0.950$ | **0.988** |
| **Inference Latency** | $< 300\text{ms}$ | **< 45ms** |

---

## 📡 REST API Reference

### Real-Time Article Authenticity Prediction
- **Endpoint:** `POST /api/predict`
- **Request Body:**
  ```json
  {
    "text": "The Federal Reserve released its quarterly economic review today..."
  }
  ```
- **Response (200 OK):**
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
        {"word": "report", "score": 1.152, "supports": "REAL"}
      ]
    },
    "meta": {
      "latency_ms": 38.42
    }
  }
  ```

---

## 🌐 Cloud Deployment on Render

This repository includes pre-configured `Procfile` and `render.yaml` manifests for instant deployment on [Render](https://render.com/).

---

## 📄 License & Academic Internship Disclaimer

Released under the **MIT License**. Developed as a 120-Hour Artificial Intelligence Internship Project.
