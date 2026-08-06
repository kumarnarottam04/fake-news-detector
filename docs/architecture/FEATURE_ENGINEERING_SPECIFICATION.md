# Master Feature Engineering Architecture & Specification

**Project Title:** Fake News Detection System  
**Document Type:** Feature Engineering Package Architecture & Vectorization Specification  
**Author:** Senior Machine Learning Engineer & AI Technical Lead  
**Target Environment:** Python 3.12+, Scikit-Learn 1.5+, SciPy Sparse Matrices  

---

## 1. Executive Summary & Architecture Overview

The **Feature Engineering Package** (`src/features/`) converts clean, normalized token strings produced by the NLP Preprocessing Pipeline into dense mathematical matrices ($N \times M$ sparse matrices) required by Machine Learning algorithms.

### Core Architectural Principles
1. **Zero Data Leakage Guarantee:** Vectorization parameters (vocabulary indices, document frequency thresholds, IDF weights, feature selection statistics) are fitted **exclusively on the training split** (`.fit()`). Validation, test, and real-time production payloads are strictly transformed (`.transform()`).
2. **Memory Efficiency via CSR Sparse Matrices:** High-dimensional N-gram vocabularies ($M = 10,000+$ features) are represented as Compressed Sparse Row (`scipy.sparse.csr_matrix`) structures, reducing memory consumption by over $95\%$ compared to dense NumPy arrays.
3. **Declarative Vectorizer Configuration:** Vectorizer hyperparameter parameters (`max_features`, `min_df`, `max_df`, `ngram_range`, `sublinear_tf`) are encapsulated in a `VectorizerConfig` dataclass object.
4. **Scikit-Learn Estimator Interface:** Implements `fit`, `transform`, `fit_transform`, and `get_feature_names_out` methods for seamless integration with downstream model trainers.

---

## 2. Complete Feature Engineering Pipeline Workflow

```
+-----------------------------------------------------------------------------------+
|                           FEATURE ENGINEERING PIPELINE                            |
|                                                                                   |
|  [ Clean Token Strings (Training Set) ]                                           |
|          |                                                                        |
|          v                                                                        |
|  ( 1. Input Validation ) -------------> Verify non-empty list of clean strings    |
|          |                                                                        |
|          v                                                                        |
|  ( 2. N-Gram Generation ) ------------> Extract Unigrams & Bigrams (1, 2)          |
|          |                                                                        |
|          v                                                                        |
|  ( 3. Document Frequency Filtering ) -> Apply min_df=2, max_df=0.95 constraints    |
|          |                                                                        |
|          v                                                                        |
|  ( 4. Vocabulary Truncation ) --------> Select Top N max_features (e.g. 10,000)   |
|          |                                                                        |
|          v                                                                        |
|  ( 5. TF-IDF Calculation ) -----------> Compute Term Frequency * Inverse Doc Freq  |
|          |                                                                        |
|          v                                                                        |
|  ( 6. Sublinear TF Scaling ) ---------> Apply TF = 1 + log(TF) to dampen high freq|
|          |                                                                        |
|          v                                                                        |
|  ( 7. Optional Feature Selection ) ---> Apply Chi-Square (SelectKBest) if enabled |
|          |                                                                        |
|          v                                                                        |
|  ( 8. CSR Matrix Formatting ) --------> Construct Scipy Compressed Sparse Row matrix|
|          |                                                                        |
|          v                                                                        |
|  ( 9. Artifact Serialization ) -------> Save joblib vectorizer & JSON metadata log|
|          |                                                                        |
|          v                                                                        |
|  [ FEATURE MATRIX READY FOR ML MODEL TRAINING ]                                   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Mathematical Foundations: CountVectorizer vs. TF-IDF Vectorizer

### 1. CountVectorizer
Counts raw occurrence frequencies $f_{t,d}$ of term $t$ in document $d$:
$$\text{Count}(t, d) = f_{t,d}$$

- **Advantage:** Highly interpretable integer counts.
- **Disadvantage:** High-frequency non-informative words dominate high vector values, masking subtle contextual keywords.

### 2. TF-IDF Vectorizer [SELECTED PRIMARY APPROACH]
Calculates the product of Term Frequency ($\text{TF}$) and Inverse Document Frequency ($\text{IDF}$):

$$\text{TF-IDF}(t, d, D) = \text{TF}(t, d) \times \text{IDF}(t, D)$$

Where:
- **Sublinear Term Frequency:**
  $$\text{TF}(t, d) = 1 + \log(f_{t,d}) \quad \text{if } f_{t,d} > 0 \text{ else } 0$$
- **Smooth Inverse Document Frequency:**
  $$\text{IDF}(t, D) = \log\left(\frac{1 + |D|}{1 + |\{d \in D : t \in d\}|}\right) + 1$$

- **Why TF-IDF Outperforms Count Vectorization:**
  - Automatically down-weights common non-discriminative terms appearing across many news articles.
  - Elevates unique informative keywords specific to Real or Fake news stories.
  - Sublinear scaling prevents an article repeating a word 50 times from having $50\times$ the weight of an article using it once.

### Vectorization Technique Comparative Matrix

| Criteria | CountVectorizer | TF-IDF Vectorizer [SELECTED] | Word Embeddings (Word2Vec) |
| :--- | :--- | :--- | :--- |
| **Mathematical Output** | Raw integer count sparse matrix | Normalized weighted float sparse matrix | Dense continuous vectors (300D) |
| **Interpretability** | Moderate | **High (Direct word weights)** | Low (Latent dimensions) |
| **Feature Dimension** | Up to $100,000+$ terms | Up to $10,000-50,000$ terms | Fixed 300 dimensions |
| **Memory Footprint** | Low (Sparse CSR) | **Very Low (Sparse CSR <15MB)** | High (Dense matrix >500MB) |
| **Handling Rare Words** | Poor (equal weight) | **Superior (High IDF multiplier)**| Low (Out-of-vocab issues) |
| **Execution Latency** | Sub-millisecond | **Sub-millisecond (<2ms)** | 10–50ms |
| **Cloud Hosting Cost** | Low | **Zero (Runs on free tier RAM)** | Moderate/High |

---

## 4. N-Gram Strategy & Feature Expansion

An N-gram is a contiguous sequence of $n$ items from a given sample of text.

- **Unigrams ($n=1$):** `["break", "official", "report", "inflation"]`  
  *Captures individual key terms.*
- **Bigrams ($n=2$):** `["official report", "report show", "inflation hit"]`  
  *Captures critical 2-word contextual phrases (e.g. "official report" vs "fake claim").*
- **Trigrams ($n=3$):** `["official report show", "white house spokesperson"]`  
  *Captures 3-word entity combinations.*

### Selected N-Gram Range: `ngram_range=(1, 2)` (Unigrams + Bigrams)
- **Justification:** Adding bigrams captures phrase context without triggering exponential vocabulary explosion or severe memory bloat caused by trigrams.

---

## 5. Feature Selection Methods ($\chi^2$ Chi-Square vs. Mutual Information)

When vocabulary dimensions exceed $50,000+$ N-grams, optional feature selection reduces noise and speeds up training.

1. **Chi-Square Test ($\chi^2$) [RECOMMENDED FEATURE SELECTOR]:**
   $$\chi^2(t, c) = \frac{N \times (AD - BC)^2}{(A+C)(B+D)(A+B)(C+D)}$$
   - Measures independence between term $t$ and class label $c$. High scores indicate strong class discriminative power.
2. **Mutual Information (MI):** Measures information gain between term occurrences and target classes. Computationally expensive on sparse text.

---

## 6. Data Leakage Prevention Architecture

```
                       +-------------------------------+
                       |   Combined Raw Dataset CSV    |
                       +-------------------------------+
                                       |
                                       v
                       +-------------------------------+
                       |  Stratified Train-Test Split  |
                       |      (80% Train / 20% Test)   |
                       +-------------------------------+
                                       |
                   +-------------------+-------------------+
                   |                                       |
                   v                                       v
    +------------------------------+        +------------------------------+
    |   X_train (40,000 Articles)  |        |    X_test (10,000 Articles)   |
    +------------------------------+        +------------------------------+
                   |                                       |
                   v                                       v
    +------------------------------+        +------------------------------+
    |  tfidf_vectorizer.fit(X_train|        | DO NOT FIT VECTORIZER HERE!  |
    |  tfidf_vectorizer.transform  |        | tfidf_vectorizer.transform   |
    +------------------------------+        +------------------------------+
                   |                                       |
                   v                                       v
    [ Sparse Matrix X_train_tfidf ]         [ Sparse Matrix X_test_tfidf ]
```

### Strict Rules to Prevent Leakage
- **Rule 1:** NEVER call `.fit()` or `.fit_transform()` on validation sets, test sets, or incoming production API requests.
- **Rule 2:** The vectorizer vocabulary and IDF weights are computed **once** during training and saved to `models/vectorizers/tfidf_vectorizer.joblib`.
- **Rule 3:** The prediction pipeline calls `.transform()` using the saved, frozen vectorizer instance.

---

## 7. Vectorizer Configuration Dataclass (`src/features/config.py`)

```python
from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class VectorizerConfig:
    """Declarative Configuration for TF-IDF Vectorizer hyperparameter tuning."""
    max_features: int = 10000
    min_df: float = 2             # Ignore terms appearing in less than 2 documents
    max_df: float = 0.95          # Ignore terms appearing in >95% of documents
    ngram_range: Tuple[int, int] = (1, 2)
    sublinear_tf: bool = True     # Use 1 + log(TF) scaling
    use_idf: bool = True
    smooth_idf: bool = True
    norm: str = 'l2'              # L2 vector normalization
    
    # Feature Selection
    enable_feature_selection: bool = False
    k_selected_features: Optional[int] = 5000
```

---

## 8. Modular Package Directory Layout

```
src/features/
├── __init__.py                     # Package exports
├── config.py                       # VectorizerConfig dataclass
├── tfidf_builder.py                # Main TF-IDF Vectorizer wrapper class
├── feature_selector.py             # Chi-Square feature selector
├── serialization.py                # Joblib vectorizer saver/loader
└── validator.py                    # Sparse matrix shape & null validators
```

---

## 9. Serialization & Metadata Specification

Every fitted vectorizer artifact saved to `models/vectorizers/` is paired with a JSON metadata sidecar:

### Metadata Sample (`models/metadata/tfidf_vectorizer_meta.json`)

```json
{
  "artifact_name": "tfidf_vectorizer.joblib",
  "build_timestamp": "2026-08-05T12:20:25Z",
  "vocabulary_size": 10000,
  "ngram_range": [1, 2],
  "sublinear_tf": true,
  "min_df": 2,
  "max_df": 0.95,
  "norm": "l2",
  "sha256_checksum": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
}
```
