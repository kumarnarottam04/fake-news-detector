# Master Enterprise AI Platform Architecture & Scalability Specification

**Project Title:** Enterprise Fake News Detection Platform  
**Document Type:** Enterprise SaaS Architecture, Database Schema, JWT Security & AI Transformer Migration Specification  
**Author:** Principal AI Architect & Enterprise Technical Director  
**Target Tech Stack:** Python 3.12+, Flask 3.0+, PostgreSQL / SQLite, SQLAlchemy ORM, JWT, Redis, Celery, Prometheus  

---

## 1. Executive Summary & Enterprise Architecture Blueprint

The **Enterprise Fake News Detection Platform** upgrades the baseline application into a multi-tenant, high-throughput AI Software-as-a-Service (SaaS) architecture. It introduces persistent database audit logs, JWT user authentication, Role-Based Access Control (RBAC), Redis prediction caching, API versioning (`/api/v1/`), Prometheus observability metrics, and a transformer (BERT/RoBERTa) deep learning migration roadmap.

### Architectural Patterns Enforced
- **Repository Pattern (`src/repositories/`):** Abstracts database queries (SQLAlchemy ORM) from business service logic, allowing seamless database migration between SQLite (development) and PostgreSQL (production).
- **Dependency Injection (`src/core/container.py`):** Injects repository and service dependencies, promoting modular testing with Pytest mocks.
- **Strategy Pattern (`src/features/` & `src/training/`):** Pluggable vectorizer strategies (TF-IDF vs BERT Embeddings) and tuning algorithms.
- **Factory Pattern (`ModelFactory` & `AppFactory`):** Centralized creation of Flask app instances and ML classifiers.

---

## 2. Enterprise Component & Layer Diagram

```
+-----------------------------------------------------------------------------------+
|                            ENTERPRISE PLATFORM ARCHITECTURE                       |
|                                                                                   |
|  [ API Gateway / Reverse Proxy (Nginx) ] ─── HTTPS & Rate Limiter                 |
|                   │                                                               |
|                   ▼                                                               |
|  [ Flask WSGI Application Server (Gunicorn) ]                                    |
|    - Blueprint Router: /api/v1/auth, /api/v1/predict, /api/v1/admin               |
|    - Security Middleware: JWT Verification, Request ID (X-Request-ID), CORS       |
|                   │                                                               |
|         ┌─────────┴─────────┐                                                     |
|         ▼                   ▼                                                     |
|  [ Service Layer ]    [ Redis Cache ] ─── Read/Write Prediction Hits (1-hr TTL)   |
|  (Prediction, Auth)         │                                                     |
|         │                   │                                                     |
|         ▼                   │                                                     |
|  [ Repository Layer ]       │                                                     |
|  (SQLAlchemy ORM)           │                                                     |
|         │                   │                                                     |
|         v                   v                                                     |
|  [ PostgreSQL / SQLite Database ] ─── Persists Users, Audit Logs, Feedback & Stats|
|                                                                                   |
|  [ Asynchronous Worker (Celery + Redis) ] ─── Daily Analytics & Cleanup Jobs     |
|                                                                                   |
|  [ Observability ] ─── Prometheus Metrics (/metrics) & Structured JSON Logger     |
+-----------------------------------------------------------------------------------+
```

---

## 3. Relational Database Schema (SQLAlchemy ORM)

The platform utilizes a relational database schema supporting users, predictions, feedback, and audit logs:

```
+-------------------------+       +------------------------------------+
|          users          |       |         prediction_logs            |
+-------------------------+       +------------------------------------+
| id (PK, UUID)           |1     *| id (PK, UUID)                      |
| email (Unique, String)  |-------| user_id (FK -> users.id, Nullable) |
| password_hash (String)  |       | article_text_hash (SHA-256)        |
| role (Enum: ADMIN, USER)|       | predicted_label (REAL / FAKE)      |
| created_at (Timestamp)  |       | confidence_score (Float)           |
+-------------------------+       | latency_ms (Float)                 |
                                  | model_version (String)             |
                                  | created_at (Timestamp)             |
                                  +------------------------------------+
                                                    | 1
                                                    |
                                                    | *
                                  +------------------------------------+
                                  |         prediction_feedback        |
                                  +------------------------------------+
                                  | id (PK, UUID)                      |
                                  | prediction_id (FK -> pred_logs.id) |
                                  | user_rating (Thumb Up / Down)      |
                                  | user_comment (Text)                |
                                  | created_at (Timestamp)             |
                                  +------------------------------------+
```

### Table DDL Specifications

```sql
-- Users Table
CREATE TABLE users (
    id VARCHAR(36) PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL DEFAULT 'USER',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Prediction Audit Logs Table
CREATE TABLE prediction_logs (
    id VARCHAR(36) PRIMARY KEY,
    user_id VARCHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    article_text_hash VARCHAR(64) NOT NULL,
    predicted_label VARCHAR(10) NOT NULL,
    confidence_score FLOAT NOT NULL,
    latency_ms FLOAT NOT NULL,
    model_version VARCHAR(20) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Prediction Feedback Loop Table
CREATE TABLE prediction_feedback (
    id VARCHAR(36) PRIMARY KEY,
    prediction_id VARCHAR(36) NOT NULL REFERENCES prediction_logs(id) ON DELETE CASCADE,
    is_correct BOOLEAN NOT NULL,
    user_comment TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Authentication & Security (JWT & RBAC)

### Authentication Endpoints (`/api/v1/auth`)

- **`POST /api/v1/auth/register`:** Hashes passwords with `bcrypt` ($12$ rounds) and creates user account.
- **`POST /api/v1/auth/login`:** Verifies credentials and emits a signed JSON Web Token (JWT) with a 24-hour expiration (`exp`).
- **Authorization Header:** Clients pass `Authorization: Bearer <JWT_TOKEN>` on protected endpoints.

### Role-Based Access Control (RBAC) Decorator Matrix

| Endpoint | Permitted Roles | Description |
| :--- | :--- | :--- |
| **`POST /api/v1/predict`** | `Anonymous`, `User`, `Admin` | Public & Authenticated Prediction Endpoint |
| **`POST /api/v1/feedback`**| `User`, `Admin` | Submit accuracy feedback on predictions |
| **`GET /api/v1/admin/analytics`**| `Admin` **ONLY** | View global prediction stats, daily counts, and error rates |
| **`GET /api/v1/admin/logs`** | `Admin` **ONLY** | Query system audit logs and exception tracebacks |

---

## 5. Caching & Performance Architecture (Redis)

```
[ POST /api/v1/predict ]
           │
           v
( Calculate SHA-256 Hash of Input Text )
           │
           v
( Query Redis Cache: `pred_cache:<SHA-256>` )
           │
     +-----+-------------------------+
     | (Cache Hit)                   | (Cache Miss)
     v                               v
[ Return Redis JSON ]     [ Execute Preprocessing & ML Model ]
(Latency < 5ms)                      │
                                     v
                          [ Store Result in Redis (TTL = 3600s) ]
                                     │
                                     v
                          [ Return JSON Response ] (Latency ~ 40ms)
```

---

## 6. API Versioning & Route Matrix

- **Version 1 (Active):** `/api/v1/predict` (TF-IDF + Logistic Regression inference engine).
- **Version 2 (Staging Roadmap):** `/api/v2/predict` (BERT Transformer embeddings + Fine-tuned Classifier).
- **Backward Compatibility:** All existing non-versioned routes (`/api/predict`) alias directly to `/api/v1/predict`.

---

## 7. Future Deep Learning & Transformer Migration Roadmap

```
+-----------------------------------------------------------------------------------+
|                        DEEP LEARNING TRANSFORMER MIGRATION                        |
|                                                                                   |
|  [ Current Pipeline: TF-IDF + Logistic Regression (95.6% Acc, <40ms Latency) ]    |
|          │                                                                        |
|          ▼ (Phase 1: Feature Extraction)                                          |
|  [ DistilBERT / Sentence-Transformers (384D Embeddings + Logistic Reg) ]          |
|          │                                                                        |
|          ▼ (Phase 2: Fine-Tuned Model)                                            |
|  [ Fine-Tuned RoBERTa-Base Classifier (PyTorch + HuggingFace Transformers) ]       |
|          │                                                                        |
|          ▼ (Phase 3: ONNX Runtime Optimization)                                   |
|  [ ONNX Runtime + Quantized INT8 Transformer (Sub-50ms CPU Latency) ]             |
+-----------------------------------------------------------------------------------+
```

---

## 8. Enterprise Observability & Metrics (`/metrics`)

The application integrates Prometheus metrics instrumentation tracking key Site Reliability Engineering (SRE) indicators:

- **`http_requests_total{endpoint, method, status}`:** Counter measuring HTTP request volume.
- **`http_request_duration_seconds{endpoint}`:** Histogram measuring latency percentiles ($P_{50}, P_{90}, P_{99}$).
- **`prediction_count_total{label="REAL|FAKE"}`:** Counter tracking real-time class distribution predictions.
- **`model_inference_duration_seconds`:** Histogram recording core ML prediction time.
