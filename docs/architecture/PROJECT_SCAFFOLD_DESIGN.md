# Enterprise Clean Architecture Scaffold Blueprint

**Project Title:** Fake News Detection System  
**Document Type:** Production Project Scaffold & Architecture Specification  
**Architecture Pattern:** Clean Layered Architecture & SOLID Domain-Driven Design  
**Target Environment:** Python 3.12+, Flask REST API, Scikit-learn NLP Engine, Render / Docker Deployment  

---

## 1. Complete Project ASCII Tree Specification

```
Fake-News-Detection/
├── .github/
│   └── workflows/
│       ├── ci.yml                          # Continuous Integration test pipeline
│       └── lint.yml                        # Automated Black, Flake8, and isort checks
├── artifacts/
│   ├── models/                             # Archived model artifacts for deployment
│   ├── vectorizers/                        # Archived TF-IDF vectorizer instances
│   ├── metrics/                            # JSON evaluation metrics reports
│   └── plots/                              # Generated ROC curves and confusion matrices
├── config/
│   ├── __init__.py                         # Package marker
│   ├── constants.py                        # System-wide static immutable constants
│   ├── logging_config.py                   # Centralized logging formatters and handlers
│   ├── paths.py                            # Centralized filesystem path resolves
│   └── settings.py                         # Environment settings loading via Pydantic/dotenv
├── data/
│   ├── raw/                                # Immutable raw original CSV datasets
│   ├── interim/                            # Intermediate transformed data frames
│   ├── processed/                          # Tokenized, cleaned, features-ready datasets
│   ├── external/                           # Third-party benchmark dataset sources
│   └── validation/                         # Holdout validation sets for regression tests
├── docs/
│   ├── api/                                # REST API OpenAPI / Swagger specifications
│   ├── architecture/                       # System architecture design & scaffold docs
│   ├── developer-guide/                    # Local environment and contributing rules
│   ├── images/                             # Architectural diagrams and UI wireframes
│   └── user-guide/                         # User manuals and usage guidelines
├── logs/
│   ├── application.log                     # General system runtime logs
│   ├── error.log                           # Exception tracebacks and critical errors
│   └── prediction.log                      # Audit trail of prediction payloads
├── models/
│   ├── trained/                            # Active production model joblib files
│   ├── vectorizers/                        # Active production TF-IDF vectorizer joblib files
│   ├── metadata/                           # Model versioning, hyperparameter JSON metadata
│   └── evaluation/                         # Model validation benchmark outputs
├── notebooks/
│   ├── 01_eda.ipynb                        # Exploratory Data Analysis & distribution plots
│   ├── 02_cleaning.ipynb                   # Preprocessing experimentation & regex benchmarking
│   ├── 03_feature_engineering.ipynb        # TF-IDF N-gram hyperparameter experiments
│   ├── 04_training_experiments.ipynb       # Model comparison (Logistic Reg vs SVM vs RF)
│   └── 05_evaluation_analysis.ipynb        # Error analysis, FP/FN inspection
├── scripts/
│   ├── build_dataset.py                    # Script to download and clean raw datasets
│   ├── train_model.py                      # CLI entry script for model training pipeline
│   ├── evaluate_model.py                   # CLI entry script for evaluation benchmarks
│   └── setup_env.sh                        # Developer virtual environment bootstrapper
├── src/
│   ├── __init__.py                         # Root source package marker
│   ├── api/                                # Presentation / REST Controller Layer
│   │   ├── __init__.py
│   │   ├── routes.py                       # HTTP Route handlers
│   │   ├── schemas.py                      # Request / Response validation schemas
│   │   └── middleware.py                   # Rate limiting, CORS, and request loggers
│   ├── core/                               # Central application core
│   │   ├── __init__.py
│   │   └── container.py                    # Dependency injection container
│   ├── exceptions/                         # Domain exception taxonomy
│   │   ├── __init__.py
│   │   └── custom_exceptions.py            # Base & specialized domain exceptions
│   ├── features/                           # Feature extraction & vectorization
│   │   ├── __init__.py
│   │   └── tfidf_builder.py                # TF-IDF Vectorizer wrapper class
│   ├── logging/                            # Logging abstraction
│   │   ├── __init__.py
│   │   └── logger_factory.py               # Logger factory and handler initializer
│   ├── preprocessing/                      # NLP Text Cleaning Pipeline
│   │   ├── __init__.py
│   │   └── text_cleaner.py                 # Tokenization, stopword removal, lemmatization
│   ├── prediction/                         # Inference Engine
│   │   ├── __init__.py
│   │   ├── model_loader.py                 # Thread-safe Singleton warm-loading manager
│   │   └── predictor.py                    # Real-time inference coordinator
│   ├── services/                           # Application Business Services
│   │   ├── __init__.py
│   │   └── prediction_service.py           # Orchestrates preprocessing, vectorizer, and model
│   ├── training/                           # Model Training Pipeline
│   │   ├── __init__.py
│   │   ├── trainer.py                      # Cross-validation & training workflow
│   │   └── hyperparameter_tuner.py         # Grid search optimization routines
│   ├── evaluation/                         # Model Evaluation Pipeline
│   │   ├── __init__.py
│   │   └── metrics_calculator.py           # Accuracy, F1, ROC-AUC, and matrix calculations
│   └── utils/                              # Utility helper modules
│       ├── __init__.py
│       ├── file_helpers.py                 # Safe IO and path validation helpers
│       ├── serialization.py                # Joblib & JSON safe loading/saving
│       └── validation_helpers.py           # Text length & format validators
├── static/                                 # Frontend static assets
│   ├── css/
│   │   └── style.css                       # Responsive glassmorphism CSS design system
│   ├── js/
│   │   └── main.js                         # REST fetch client & DOM dynamic updates
│   └── images/
│       └── favicon.ico                     # Web application icon
├── templates/                              # Presentation HTML templates
│   └── index.html                          # Main Single Page Application view template
├── tests/                                  # Test Suite
│   ├── __init__.py
│   ├── conftest.py                         # Pytest shared fixtures and client setup
│   ├── fixtures/                           # Sample text payloads & mock vectorizers
│   │   └── sample_articles.json
│   ├── integration/                        # REST API endpoint tests
│   │   └── test_api_routes.py
│   └── unit/                               # Preprocessing & inference unit tests
│       ├── test_text_cleaner.py
│       ├── test_model_loader.py
│       └── test_predictor.py
├── .editorconfig                           # Cross-editor formatting consistency
├── .env.example                            # Template environment variable configuration
├── .gitignore                              # Git tracking exclusion rules
├── app.py                                  # Flask WSGI Server entry point
├── Procfile                                # Gunicorn WSGI startup configuration for cloud
├── render.yaml                             # Render Infrastructure-as-Code blueprint
├── pyproject.toml                          # Black, isort, and Pytest configuration
├── requirements.txt                        # Production & Development pinned dependencies
├── runtime.txt                             # Python runtime version lock (e.g. python-3.12.0)
├── LICENSE                                 # MIT Open-Source License
└── README.md                               # Project documentation & quickstart overview
```

---

## 2. Detailed Explanation of Root Directories

| Folder Name | Purpose & Functionality | Permitted File Types |
| :--- | :--- | :--- |
| **`artifacts/`** | Long-term immutable binary & metrics storage for model releases, training plots, and evaluation reports. | `.joblib`, `.json`, `.png`, `.csv` |
| **`config/`** | Centralized application configuration, path resolvers, static constants, and logging settings. | `.py` |
| **`data/`** | Multi-stage data processing pipeline (Raw $\rightarrow$ Interim $\rightarrow$ Processed). | `.csv`, `.parquet`, `.json` |
| **`docs/`** | Comprehensive developer, API, user, and architectural documentation. | `.md`, `.png`, `.yaml` |
| **`logs/`** | Dual-output rotating application, error, and prediction audit logs. | `.log` |
| **`models/`** | Active runtime model binary artifacts, vectorizers, and version metadata. | `.joblib`, `.json` |
| **`notebooks/`** | Sequenced exploratory data analysis, cleaning experiments, and model prototyping. | `.ipynb` |
| **`scripts/`** | Command-line operational scripts for automation, data building, and manual training. | `.py`, `.sh` |
| **`src/`** | Production source code organized into modular Clean Architecture layers. | `.py` |
| **`static/` & `templates/`**| Frontend presentation view layer (HTML5, CSS3, JavaScript). | `.html`, `.css`, `.js`, `.ico` |
| **`tests/`** | Automated test suite containing unit tests, integration tests, and shared fixtures. | `.py`, `.json` |

---

## 3. Modular `src/` Package Architecture & Dependency Directions

```
                           +------------------------+
                           |  Presentation Layer    |
                           |       (src/api/)       |
                           +------------------------+
                                       |
                                       v
                           +------------------------+
                           |   Application Service  |
                           |    (src/services/)     |
                           +------------------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
+------------------------------------+   +------------------------------------+
|         NLP Preprocessing          |   |          ML Inference Engine       |
|    (src/preprocessing/, features/) |   |       (src/prediction/, models/)   |
+------------------------------------+   +------------------------------------+
                   |                                       |
                   +-------------------+-------------------+
                                       |
                                       v
                           +------------------------+
                           |  Core Infrastructure   |
                           | (config/, exceptions/, |
                           |  utils/, logging/)     |
                           +------------------------+
```

### Layer Responsibilities & Dependency Rules

1. **`src/api/` (Presentation Controller Layer):**
   - **Responsibility:** Handles HTTP requests, parses JSON payloads via `schemas.py`, delegates logic to `services/`, and formats HTTP responses.
   - **Allowed Imports:** `src/services/`, `src/exceptions/`, `src/utils/`, `config/`.
   - **Forbidden Imports:** Direct access to `src/training/` or raw database calls.

2. **`src/services/` (Application Service Layer):**
   - **Responsibility:** Orchestrates business workflows (e.g. `PredictionService` calling text cleaners, vectorizer transformers, and inference predictors).
   - **Allowed Imports:** `src/preprocessing/`, `src/features/`, `src/prediction/`, `src/exceptions/`, `config/`.

3. **`src/preprocessing/` & `src/features/` (NLP & Feature Layer):**
   - **Responsibility:** Text normalization (lowercasing, regex cleaning, NLTK stopword filtering, lemmatization) and TF-IDF feature matrix transformation.
   - **Allowed Imports:** `src/utils/`, `src/exceptions/`, `config/`.
   - **Forbidden Imports:** `src/api/`, `src/prediction/`.

4. **`src/prediction/` & `src/training/` (Machine Learning Engine):**
   - **Responsibility:** Thread-safe Singleton model loading (`model_loader.py`), model execution (`predictor.py`), model training (`trainer.py`), and evaluation (`metrics_calculator.py`).
   - **Allowed Imports:** `src/features/`, `src/preprocessing/`, `src/exceptions/`, `config/`.

5. **`src/exceptions/`, `src/utils/`, `src/logging/`, `config/` (Core Utilities):**
   - **Responsibility:** Independent infrastructure modules supplying exception definitions, logging factories, file I/O helpers, and configuration settings.
   - **Allowed Imports:** Standard library & third-party libraries **ONLY** (Zero internal domain dependencies to prevent circular imports).

---

## 4. Multi-Stage Data Pipeline Architecture

```
[ External News Sources ]
           |
           v
   +---------------+
   |   data/raw/   |  --> Read-only original CSV dataset files (WELFake / ISOT)
   +---------------+
           |
           | Script: scripts/build_dataset.py
           v
 +-------------------+
 |   data/interim/   |  --> Intermediate data with nulls dropped & text concatenated
 +-------------------+
           |
           | Script: src/preprocessing/text_cleaner.py
           v
 +-------------------+
 |  data/processed/  |  --> Cleaned, tokenized, and lemmatized datasets ready for ML
 +-------------------+
           |
           +-----------------------------+
           |                             |
           v                             v
 +-------------------+         +-------------------+
 | data/validation/  |         |   data/external/  |
 | (Holdout Test)    |         | (Benchmark Data)  |
 +-------------------+         +-------------------+
```

---

## 5. Model Storage, Naming & Versioning Strategy

### Directory Specification (`models/`)
- **`models/trained/model_v1.0.0.joblib`:** Production binary model artifact.
- **`models/vectorizers/tfidf_v1.0.0.joblib`:** Matching TF-IDF vectorizer vocabulary artifact.
- **`models/metadata/model_v1.0.0_meta.json`:** JSON metadata storing model type, hyperparameters, dataset SHA-256 hash, accuracy metrics, and build timestamp.

### Semantic Artifact Naming Convention
```
model_<major>.<minor>.<patch>.joblib
tfidf_<major>.<minor>.<patch>.joblib
```
- **Major Version:** Breaking change in feature vocabulary dimension or NLP pipeline algorithm.
- **Minor Version:** Re-trained model with hyperparameter updates or expanded training dataset.
- **Patch Version:** Bug fix or small validation fine-tuning.

---

## 6. Centralized Custom Exception Taxonomy

All custom domain exceptions inherit from a base `FakeNewsDetectorException`, ensuring unified exception catching in API controllers:

```
                      +-----------------------------+
                      | FakeNewsDetectorException   |
                      +-----------------------------+
                                     |
    +-----------------+--------------+-----------------+-----------------+
    |                 |                                |                 |
    v                 v                                v                 v
+---------------+ +-------------------+     +------------------+ +-----------------+
|ValidationError| | ModelLoadError    |     | PredictionError  | |ConfigurationError|
+---------------+ +-------------------+     +------------------+ +-----------------+
```

### Exception Usage Rules
1. **`ValidationError`:** Raised when input text is empty, shorter than 50 characters, or exceeds payload size limits. Maps to **HTTP 400 Bad Request**.
2. **`ModelLoadError`:** Raised when `.joblib` artifacts are missing, corrupt, or unreadable during startup. Maps to **HTTP 503 Service Unavailable**.
3. **`PredictionError`:** Raised when feature vector transformation or probability matrix calculations fail during runtime. Maps to **HTTP 500 Internal Error**.
4. **`ConfigurationError`:** Raised when mandatory environment variables or directory paths are invalid. Prevents server startup.
5. **`DataError`:** Raised when training CSV datasets contain missing labels or corrupted text columns.

---

## 7. Logging Architecture & Rotation Policy

### Multi-Log File Strategy (`logs/`)

1. **`logs/application.log`:** Captures `INFO` and `DEBUG` events regarding application startup, HTTP request routing, and system status.
2. **`logs/prediction.log`:** Captures audit records of every prediction request (sanitized input length, predicted label, confidence percentage, execution latency).
3. **`logs/error.log`:** Captures `ERROR` and `CRITICAL` exception stack traces.

### Log Rotation Policy
- **Type:** Size-based `RotatingFileHandler`.
- **Max File Size:** `5 MB` ($5 \times 1024 \times 1024$ bytes) per file.
- **Backup Count:** `5` backup archives retained before automatic purge (`application.log.1`, `application.log.2`).

---

## 8. Development & Architectural Best Practices

### SOLID Principles Application

- **Single Responsibility Principle (SRP):** `TextCleaner` *only* cleans text; `ModelLoader` *only* manages artifact loading; `Predictor` *only* runs inference logic.
- **Open/Closed Principle (OCP):** New classification models (e.g., SVM or XGBoost) can be added without modifying the HTTP controller or preprocessing interface.
- **Liskov Substitution Principle (LSP):** Vectorizers and classifiers adhere to standard Scikit-learn estimator interface contracts (`fit`, `transform`, `predict`).
- **Interface Segregation Principle (ISP):** API endpoints consume lean schemas (`schemas.py`) tailored strictly to required request parameters.
- **Dependency Inversion Principle (DIP):** Higher-level service layers depend on abstract processing interfaces rather than concrete file system paths.

### Additional Design Rules
- **DRY (Don't Repeat Yourself):** Centralized text cleaning and file serialization utilities shared between training scripts and API inference.
- **KISS (Keep It Simple, Stupid):** Prefer lightweight, highly interpretable models (Logistic Regression + TF-IDF) over complex over-engineered neural networks.
- **YAGNI (You Aren't Gonna Need It):** Avoid implementing multi-tenant database layers or complex message queues until traffic volume explicitly requires scaling.

---

## 9. Future Scalability Roadmap

```
+-----------------------------------------------------------------------------------+
|                            FUTURE ARCHITECTURE ROADMAP                            |
|                                                                                   |
|   +-------------------+    +---------------------+    +-----------------------+   |
|   |  Containerization | -> | Async Task Queues   | -> | Deep Learning Models  |   |
|   |  (Docker Compose) |    | (Celery + Redis)    |    | (BERT / RoBERTa Transformer)|
|   +-------------------+    +---------------------+    +-----------------------+   |
|                                                                                   |
|   +-------------------+    +---------------------+    +-----------------------+   |
|   | Database Audit    | -> | OAuth2 Security     | -> | Kubernetes Cluster    |   |
|   | (PostgreSQL/SQLAlchemy)|(JWT User Auth)      |    | (Horizontal Auto Scale)|
|   +-------------------+    +---------------------+    +-----------------------+   |
+-----------------------------------------------------------------------------------+
```

---

## 10. Beginner Implementation Order & Step-by-Step Roadmap

1. **Step 1 (Scaffold Setup):** Verify directory tree creation and configure `.env`, `config/paths.py`, and `config/settings.py`.
2. **Step 2 (Logging & Exceptions):** Implement `src/exceptions/custom_exceptions.py` and `src/logging/logger_factory.py`.
3. **Step 3 (NLP Preprocessing Engine):** Build `src/preprocessing/text_cleaner.py` and test using `notebooks/02_cleaning.ipynb`.
4. **Step 4 (Model Training Pipeline):** Build `src/features/tfidf_builder.py` and `src/training/trainer.py`. Execute `scripts/train_model.py` to generate initial model artifacts in `models/trained/`.
5. **Step 5 (Inference Service):** Build `src/prediction/model_loader.py` and `src/prediction/predictor.py`.
6. **Step 6 (Flask REST API Controller):** Build `src/api/routes.py` and connect `app.py`.
7. **Step 7 (Responsive UI View):** Connect `templates/index.html` and `static/` styling to Flask routes.
8. **Step 8 (Automated Testing):** Execute pytest suite across `tests/unit/` and `tests/integration/`.
9. **Step 9 (Cloud Deployment):** Deploy repository to Render using `render.yaml` and `Procfile`.
