# Master Production Deployment, DevOps & Infrastructure Specification

**Project Title:** Fake News Detection System  
**Document Type:** Production Cloud Deployment, DevOps, Infrastructure-as-Code & CI/CD Specification  
**Author:** Principal DevOps Engineer & SRE Lead  
**Target Environments:** Render Web Service, Railway, Docker, GitHub Actions CI/CD  

---

## 1. Executive Summary & 12-Factor App Compliance

This document outlines the production deployment, infrastructure-as-code (IaC), automated testing CI/CD pipeline, and site reliability engineering (SRE) specifications for hosting the **Fake News Detection System**.

### 12-Factor App Methodology Adherence
1. **Codebase:** One repository tracked in version control, deployed to multiple environments (Development, Staging, Production).
2. **Dependencies:** Explicitly declared and isolated dependencies pinned in `requirements.txt`.
3. **Config:** Strict separation of config from code via environment variables (`.env`, Render Environment Settings).
4. **Backing Services:** Model artifacts and file storage treated as attached resource paths (`models/`).
5. **Build, Release, Run:** Strict separation between build phase (`pip install`), release phase (`gunicorn` boot), and run phase.
6. **Stateless Processes:** Flask app instances run as zero-state processes; warm model memory is loaded at cold-start.
7. **Port Binding:** Self-contained web service binding to `$PORT` via Gunicorn WSGI.
8. **Concurrency:** Scale out via Gunicorn worker processes (`--workers 2 --threads 2`).
9. **Disposability:** Fast startup (<3s) and graceful shutdown handling (`SIGTERM`).
10. **Logs:** Logs treated as unbuffered event streams routed to stdout and rotating log files.

---

## 2. Infrastructure Architecture Diagram

```
+-----------------------------------------------------------------------------------+
|                                PRODUCTION DEPLOYMENT                              |
|                                                                                   |
|  [ GITHUB REPOSITORY ] ──────────────────── Push to main branch                  |
|          │                                                                        |
|          ▼                                                                        |
|  [ GITHUB ACTIONS CI/CD ]                                                         |
|    - Step 1: Checkout Code                                                        |
|    - Step 2: Set up Python 3.12                                                   |
|    - Step 3: Install Pinned Requirements                                          |
|    - Step 4: Run Code Quality Checks (Black, Flake8, isort)                      |
|    - Step 5: Execute Pytest Suite (Unit + Integration Tests)                      |
|          │                                                                        |
|          ▼ (On CI Pass)                                                           |
|  [ RENDER CLOUD AUTO-DEPLOYMENT ]                                                 |
|    - Read render.yaml blueprint                                                   |
|    - Execute Build Command: `pip install -r requirements.txt && NLTK downloads`  |
|    - Launch WSGI Server: `gunicorn -c gunicorn.conf.py app:app`                  |
|          │                                                                        |
|          ▼                                                                        |
|  [ RENDER WEB SERVICE INSTANCE (Free Tier: 512 MB RAM) ]                          |
|    - Gunicorn Master Process                                                      |
|        ├── Worker Process 1 (2 Threads)                                           |
|        └── Worker Process 2 (2 Threads)                                           |
|    - Warm Model Singleton loaded in RAM (<250 MB total memory)                    |
|    - Health Check Ping: GET /health (HTTP 200 OK)                                 |
|          │                                                                        |
|          ▼                                                                        |
|  [ PUBLIC HTTPS ENDPOINT: https://fake-news-detector.onrender.com ]              |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Environment Variables Specification (`.env.example`)

All secrets and environment-dependent variables are externalized:

| Variable Name | Required | Default Value (Dev) | Production Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`FLASK_ENV`** | **Yes** | `development` | `production` | Environment profile toggle |
| **`SECRET_KEY`** | **Yes** | `dev-secret-key-change-me` | `[SECURE_RANDOM_UUID]`| Flask session & CSRF signing key |
| **`PORT`** | **Yes** | `5000` | `$PORT` (Allocated) | Web server listener port |
| **`LOG_LEVEL`** | No | `DEBUG` | `INFO` | Logging verbosity level |
| **`MODEL_PATH`** | **Yes** | `models/model.joblib` | `models/model.joblib` | Path to trained model joblib file |
| **`VECTORIZER_PATH`**| **Yes** | `models/tfidf_vectorizer.joblib`| `models/tfidf_vectorizer.joblib`| Path to TF-IDF vectorizer joblib |
| **`MAX_CONTENT_LENGTH`**| No| `1048576` (1MB) | `1048576` (1MB) | Maximum HTTP request payload cap |

---

## 4. Production Gunicorn WSGI Configuration (`gunicorn.conf.py`)

To optimize memory consumption on Render's 512 MB RAM instance while maintaining high request concurrency:

```python
import os
import multiprocessing

# Server Socket
bind = f"0.0.0.0:{os.getenv('PORT', '5000')}"

# Concurrency & Worker Model
# Formula: (2 * CPUs) + 1 for standard; hardcoded 2 for 512MB RAM cap
workers = int(os.getenv('WEB_CONCURRENCY', '2'))
threads = 2
worker_class = 'gthread'

# Timeouts
timeout = 60
keepalive = 5

# Process Naming
proc_name = 'fake_news_detector_gunicorn'

# Logging
accesslog = '-'   # Stdout
errorlog = '-'    # Stderr
loglevel = os.getenv('LOG_LEVEL', 'info').lower()

# Server Mechanics
preload_app = True  # Load model artifacts ONCE in master process before worker fork
```

---

## 5. Render Infrastructure-as-Code Manifest (`render.yaml`)

```yaml
services:
  - type: web
    name: fake-news-detector
    env: python
    region: oregon
    plan: free
    buildCommand: "pip install -r requirements.txt && python -c \"import nltk; nltk.download('stopwords'); nltk.download('wordnet')\""
    startCommand: "gunicorn -c gunicorn.conf.py app:app"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PYTHON_VERSION
        value: 3.12.0
      - key: LOG_LEVEL
        value: INFO
      - key: SECRET_KEY
        generateValue: true
```

---

## 6. Production Containerization (`Dockerfile`)

```dockerfile
# Multi-stage lightweight Python 3.12 Slim base image
FROM python:3.12-slim as builder

WORKDIR /app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final Runtime Image
FROM python:3.12-slim

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application files
COPY . .

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

# Create non-root system user for security
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 5000

ENV FLASK_ENV=production
ENV PORT=5000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:5000/health || exit 1

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
```

---

## 7. GitHub Actions Automated CI/CD Workflow (`.github/workflows/ci.yml`)

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test-and-lint:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Set up Python 3.12
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'
          cache: 'pip'

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          python -c "import nltk; nltk.download('stopwords'); nltk.download('wordnet')"

      - name: Code Style Check (Black & Flake8)
        run: |
          black --check src/ app.py
          flake8 src/ app.py --max-line-length=88

      - name: Execute Automated Test Suite (Pytest)
        run: |
          pytest tests/ -v --tb=short
```

---

## 8. Incident Recovery & Rollback Plan

1. **Deployment Failure (Build Crash / Failed Health Check):**
   - Render automatically cancels rolling release if `/health` returns non-200 within 60 seconds; traffic remains on previous working deployment.
2. **Missing Model Artifact Fallback:**
   - If `models/model.joblib` is deleted, `app.py` auto-initializes `train_pipeline()`, building a fresh benchmark model on cold start.
3. **Manual Version Rollback:**
   - On Render Dashboard $\rightarrow$ Deploys $\rightarrow$ Click previous successful commit $\rightarrow$ Select **"Rollback to this deploy"**.

---

## 9. Final Deployment Verification Checklist

- [x] **Pinned Dependencies:** All packages pinned in `requirements.txt`.
- [x] **Python Runtime Lock:** `runtime.txt` specifies `python-3.12.0`.
- [x] **WSGI Configuration:** `gunicorn.conf.py` tuned for multi-threaded execution.
- [x] **Cloud IaC Blueprint:** `render.yaml` configured with auto NLTK downloads.
- [x] **Containerization:** Production `Dockerfile` and `.dockerignore` created.
- [x] **Automated CI/CD:** `.github/workflows/ci.yml` configured for linting and Pytest.
- [x] **Health Check:** `/health` endpoint returns JSON uptime and model status.
- [x] **Security Hardening:** Payload cap (1MB), CORS, and security headers active.
