# Master Full-Stack Integration Architecture Specification

**Project Title:** Fake News Detection System  
**Document Type:** End-to-End Full-Stack Integration, API Communication & State Management Specification  
**Author:** Principal Full-Stack AI Engineer & Technical Lead  
**Target Tech Stack:** Flask 3.0+ REST API, Vanilla ES6+ Fetch API, HTML5, Glassmorphism CSS3  

---

## 1. Executive Summary & Application Flow

This document details the end-to-end integration binding the **Flask WSGI REST API Backend** to the **Responsive Glassmorphism Presentation Frontend**.

### Complete End-to-End Execution Sequence

```
+-----------------------------------------------------------------------------------+
|                        END-TO-END APPLICATION EXECUTION FLOW                      |
|                                                                                   |
|  [ User Opens Web Portal ] -----------------> Browser loads index.html & main.js   |
|          |                                                                        |
|          v                                                                        |
|  [ User Enters Article & Clicks "Analyze" ]                                       |
|          |                                                                        |
|          v                                                                        |
|  ( 1. Client-Side Validation ) -------------> Check non-empty, len >= 50 chars    |
|          |                                                                        |
|          v                                                                        |
|  ( 2. State & UI Lock ) --------------------> Disable button, show spinner       |
|          |                                                                        |
|          v                                                                        |
|  ( 3. Async Fetch Request ) ----------------> POST /api/predict { "text": "..." } |
|          |                                                                        |
|          v                                                                        |
|  ( 4. Flask WSGI Router ) ------------------> Rate limit check & payload length check|
|          |                                                                        |
|          v                                                                        |
|  ( 5. NLP Preprocessing Engine ) -----------> Lowercase, Regex HTML/URL removal,  |
|          |                                    NLTK Stopwords & Lemmatization      |
|          |                                                                        |
|          v                                                                        |
|  ( 6. TF-IDF & Model Inference ) -----------> Compute 1x10,000 sparse matrix,     |
|          |                                    P(Real), P(Fake), top word weights  |
|          |                                                                        |
|          v                                                                        |
|  ( 7. JSON Response Serialization ) --------> Emit HTTP 200 OK + Security Headers  |
|          |                                                                        |
|          v                                                                        |
|  ( 8. Client UI Render ) -------------------> Animate Confidence Gauge, render    |
|          |                                    Badge color & Keyword Badges        |
|          v                                                                        |
|  [ USER VIEWS PREDICTION & EXPLANATION ]                                          |
+-----------------------------------------------------------------------------------+
```

---

## 2. API Communication & Request / Response Specs

### Request Payload (`POST /api/predict`)
```json
{
  "text": "The Federal Reserve released its quarterly economic review today, highlighting sustained growth across major industrial sectors. Inflation rates held steady while job creation figures exceeded initial projections by two percent."
}
```

### Standardized Success Response (`HTTP 200 OK`)
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
    "timestamp": "2026-08-05T12:28:23Z",
    "model_version": "1.0.0"
  }
}
```

---

## 3. Client-Side API Communication Engine (`static/js/main.js`)

The JavaScript client encapsulates request dispatch, timeout cancellation (`AbortController`), retry logic, and error handling:

```javascript
/**
 * Async API Fetch Client with Timeout and Retry Capabilities
 */
async function fetchPrediction(textPayload, options = {}) {
    const { timeoutMs = 10000, maxRetries = 2 } = options;
    const url = '/api/predict';

    for (let attempt = 0; attempt <= maxRetries; attempt++) {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

        try {
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ text: textPayload }),
                signal: controller.signal
            });

            clearTimeout(timeoutId);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error ? data.error.message : `HTTP Error ${response.status}`);
            }

            return data;

        } catch (err) {
            clearTimeout(timeoutId);
            
            if (err.name === 'AbortError') {
                throw new Error('Request timed out after 10 seconds. Please try again.');
            }
            
            if (attempt === maxRetries) {
                throw err;
            }
            
            // Wait 1 second before retrying
            await new Promise(res => setTimeout(res, 1000));
        }
    }
}
```

---

## 4. Error Handling & Status Mapping Matrix

| Scenario / Error Type | HTTP Status Code | Frontend Error Alert Display | Actionable User Guidance |
| :--- | :--- | :--- | :--- |
| **Short Input (<50 chars)**| N/A (Client-Side) | *"Article text must be at least 50 characters long."* | Prompt user to paste full article body |
| **Payload Too Large** | `413 Payload Too Large` | *"Article text exceeds maximum size limit (1 MB)."* | Prompt user to reduce article length |
| **Rate Limit Exceeded** | `429 Too Many Requests` | *"Rate limit exceeded (30 req/min). Please wait 60s."*| Temporarily disable submit button for 60s |
| **Model Unavailable** | `503 Service Unavailable`| *"AI Model initialization in progress. Retry shortly."*| Auto-retry request after 5 seconds |
| **Network Disconnection** | `0 / Fetch Error` | *"Network connection lost. Check your internet."* | Provide manual "Retry Request" button |

---

## 5. Security & XSS Prevention Layer

1. **Strict HTML Escaping on Dynamic DOM Injection:** All text strings originating from user inputs or server responses are sanitized before DOM insertion using text nodes or escaping functions:
   ```javascript
   function escapeHtml(str) {
       return String(str).replace(/[&<>"']/g, (m) => ({
           '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;'
       })[m]);
   }
   ```
2. **Double Submission Prevention:** When the form is submitted, `btnSubmit.disabled = true` is executed immediately, preventing duplicate request spam.
3. **Payload Sanitization:** Flask backend strips script tags and XML structures before feeding text into NLTK cleaners.

---

## 6. End-to-End Integration Testing Strategy

The integrated application is audited against five core test categories:

- [x] **E2E Smoke Test:** Input sample text $\rightarrow$ Submit form $\rightarrow$ Verify real-time prediction badge renders (**REAL** / **FAKE**) within $<300\text{ms}$.
- [x] **Validation Boundary Test:** Input 49 characters $\rightarrow$ Verify client alert catches input $\rightarrow$ Verify zero API calls dispatched.
- [x] **Rate Limit Test:** Dispatch $>30$ fast requests $\rightarrow$ Verify HTTP 429 JSON returned $\rightarrow$ Verify alert box displays rate limit warning.
- [x] **XSS Injection Test:** Input `<script>alert('xss')</script>` text $\rightarrow$ Verify zero script execution; text is safely lowercased and cleaned.
- [x] **Theme Persistence Test:** Toggle dark/light mode $\rightarrow$ Reload page $\rightarrow$ Verify theme setting persists.
