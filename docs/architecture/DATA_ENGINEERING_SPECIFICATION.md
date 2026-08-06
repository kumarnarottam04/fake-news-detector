# Master Data Engineering & Dataset Specification Document

**Project Title:** Fake News Detection System  
**Document Type:** Dataset Selection, Data Ingestion, Data Validation & Management Architecture  
**Role:** Senior Data Engineer & AI Technical Lead  
**Target Environment:** Python 3.12+, Data Validation Pipeline, Metadata Tracker, Version Control  

---

## 1. Executive Data Strategy & Objectives

The integrity and generalization capability of any Machine Learning classification model is strictly bounded by the quality of its underlying dataset ("Garbage In, Garbage Out"). This document specifies an enterprise-grade Data Engineering & Management Pipeline designed to ingest, validate, profile, and version external fake news datasets before any Natural Language Processing (NLP) or Machine Learning model training occurs.

### Core Data Pipeline Objectives
- **Reproducibility:** Deterministic ingestion and automated checksum validation ensuring identical dataset states across developer environments.
- **Data Integrity & Schema Enforcement:** Strict data validation rules preventing missing text, corrupted encodings, or invalid label distributions from contaminating the ML pipeline.
- **Auditability & Traceability:** Automated JSON metadata tracking for dataset versions, source origins, license compliance, and cryptographic hashes.
- **Immutability:** Isolation of original raw datasets in read-only storage (`data/raw/`) to preserve ground truth.

---

## 2. Public Dataset Comparative Analysis

We evaluated five prominent publicly available benchmark datasets for Fake News Detection research across criteria including sample volume, feature richness, label balance, license permissions, and production suitability.

### Dataset Benchmark Comparison Matrix

| Feature / Criteria | 1. ISOT Fake News | 2. Kaggle (WELFake) | 3. LIAR Dataset | 4. FakeNewsNet | 5. BuzzFeed News |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Source** | University of Victoria | Kaggle / IEEE DataPort | PolitiFact Fact-Checker | GitHub / Academic Repo | BuzzFeed Fact-Check |
| **Total Records** | **44,898 articles** | **72,134 articles** | **12,836 statements** | **23,196 articles** | **1,827 posts** |
| **Real Class Count** | 21,417 (47.7%) | 35,028 (48.6%) | 4,500 (35.1%) | 17,441 (75.2%) | 1,669 (91.4%) |
| **Fake Class Count** | 23,481 (52.3%) | 37,106 (51.4%) | 8,336 (64.9%) | 5,755 (24.8%) | 158 (8.6%) |
| **Granularity** | Full Article Body | Full Article Body | Short Statements | Full Article + Social | Social Media Posts |
| **Label Type** | Binary (0 / 1) | Binary (0 / 1) | 6-Class Multi-label | Binary (0 / 1) | 4-Class Scale |
| **Key Features** | Title, Text, Subject, Date | Title, Text, Label | Statement, Speaker, Context | Title, Text, Tweets, Images | Title, Body Text, URL |
| **License** | Open Academic Use | CC0 Public Domain | Creative Commons | Academic Only | Open Source |
| **Class Imbalance** | **Balanced (1:1.09)** | **Balanced (1:1.06)** | Imbalanced | Severe (1:3.03) | Extreme (1:10.5) |
| **Beginner Friendly** | **Very High** | **Very High** | Moderate | Low (Requires Scraping)| Low (Small Sample) |
| **Production Grade**| **High** | **Very High** | Moderate | High (Multi-modal) | Low |

---

### In-Depth Dataset Evaluations

#### 1. ISOT Fake News Dataset (University of Victoria)
- **Source:** Collected by the Information Security and Object Technology (ISOT) lab from Reuters.com (Real) and unflagged fake news sites (2016–2017).
- **Advantages:** Clean text, balanced class distribution, includes full article text and headlines.
- **Limitations:** Real news contains "Reuters" publisher tags in body text, which must be stripped to prevent model shortcut learning (data leakage).

#### 2. Kaggle / WELFake Dataset [RECOMMENDED PRIMARY DATASET]
- **Source:** Combined benchmark dataset merging Kaggle Fake News, McIntire, Reuters, and NewsAPI datasets.
- **Advantages:** Massive sample size (72,134 records), highly balanced class ratio ($51.4\%$ Fake vs $48.6\%$ Real), rich combined headline and article body text, public domain CC0 license.
- **Limitations:** Contains small percentage of blank body text where only headlines exist (handled via automated column fallback during data ingestion).

#### 3. LIAR Dataset
- **Source:** Short political statements extracted from PolitiFact.
- **Advantages:** Fine-grained 6-way classification labels (*pants-on-fire, false, barely-true, half-true, mostly-true, true*).
- **Limitations:** Evaluates short 1–2 sentence statements rather than full news articles; low word count per record reduces TF-IDF feature richness.

#### 4. FakeNewsNet
- **Source:** GossipCop and PolitiFact article collections with social media engagement metadata.
- **Advantages:** Rich multi-modal features including tweet retweets and user demographic networks.
- **Limitations:** Requires scraping raw article body URLs (many of which are now offline 404 links).

#### 5. BuzzFeed News Dataset
- **Source:** Facebook posts published by 9 news outlets during the 2016 US election campaign.
- **Advantages:** High-veracity human fact-checking labels.
- **Limitations:** Extremely small dataset (1,827 samples) with severe class imbalance ($8.6\%$ fake news), unsuitable for training robust ML classifiers.

---

### Final Dataset Recommendation & Justification

> [!IMPORTANT]
> **Primary Selection for Project: Kaggle WELFake / ISOT Dataset Combo**
> - **Justification:** Combines large sample size ($>70,000$ articles), perfectly balanced binary labels, full-length journalistic text bodies, and CC0 open license. It provides ideal high-dimensional TF-IDF feature density required for accurate linear and ensemble machine learning classification.

---

## 3. Data Directory Architecture

```
data/
├── archive/                        # Compressed zipped archives of original downloads
├── dictionary/                     # Automated data dictionary JSON specifications
├── external/                       # Third-party benchmark datasets (LIAR, BuzzFeed)
├── interim/                        # Staged datasets with standardized schemas
├── metadata/                       # Automated JSON metadata logs (checksums, record counts)
├── processed/                      # Cleaned, tokenized datasets ready for EDA & ML
├── raw/                            # Read-only original downloaded CSV datasets
├── samples/                        # Small sample JSON datasets (100 rows) for unit testing
└── validation/                     # Holdout validation sets for model regression tests
```

### Folder Responsibilities & Read/Write Access Matrix

| Folder Path | Access Mode | Primary Owner Script | Purpose |
| :--- | :--- | :--- | :--- |
| **`data/archive/`** | Write-Once / Read-Only | Ingestion Script | Stores original `.zip` or `.tar.gz` downloads |
| **`data/raw/`** | **Read-Only (Strict)** | Ingestion Script | Holds pristine uncompressed CSV files |
| **`data/interim/`** | Read / Write | Ingestion / Staging Script | Holds standardized schema CSVs before NLP |
| **`data/processed/`** | Read / Write | Preprocessing Pipeline | Holds clean tokenized datasets ready for training |
| **`data/metadata/`** | Write-Append | Metadata Generator | Stores JSON version metadata and SHA-256 hashes |
| **`data/dictionary/`**| Read-Only | Documentation Manager | Houses machine-readable Data Dictionary schemas |
| **`data/samples/`** | Read-Only | Test Suite | Houses fast mock datasets for unit/integration tests |

---

## 4. End-to-End Data Ingestion Pipeline Workflow

```
+-----------------------------------------------------------------------------------+
|                               DATA INGESTION PIPELINE                             |
|                                                                                   |
|  [ Download Source ]                                                              |
|          |                                                                        |
|          v                                                                        |
|  ( 1. Download Dataset Script ) ---> Fetch raw archive from remote repository     |
|          |                                                                        |
|          v                                                                        |
|  ( 2. Integrity Check ) -----------> Calculate SHA-256 Checksum vs Reference Hash |
|          |                                                                        |
|          v                                                                        |
|  ( 3. File & Encoding Validation ) -> Verify file extension (.csv) & UTF-8 encoding|
|          |                                                                        |
|          v                                                                        |
|  ( 4. Schema & Header Check ) ----> Validate required column names & data types   |
|          |                                                                        |
|          v                                                                        |
|  ( 5. Duplicate Detection ) -------> Identify duplicate rows & exact text matches  |
|          |                                                                        |
|          v                                                                        |
|  ( 6. Missing Value Analysis ) ----> Measure null counts across title/text columns |
|          |                                                                        |
|          v                                                                        |
|  ( 7. Label Sanitization ) -------> Normalize binary labels to integer (0 or 1)   |
|          |                                                                        |
|          v                                                                        |
|  ( 8. Write to Raw Directory ) ---> Save immutable copy to data/raw/              |
|          |                                                                        |
|          v                                                                        |
|  ( 9. Metadata Generation ) ------> Emit JSON audit file to data/metadata/        |
|          |                                                                        |
|          v                                                                        |
|  [ READY FOR EDA & CLEANING ]                                                     |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

---

## 5. Standardized Data Schema Specification

To standardize heterogeneous external datasets, all ingested raw datasets are mapped into a unified target schema:

| Column Name | Target Data Type | Nullable | Validation Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| **`article_id`** | `String (UUIDv4)` | **No** | Unique string identifier | Unique primary key for each article record |
| **`title`** | `String (UTF-8)` | Yes | Max 500 characters | Headline of the news article |
| **`text`** | `String (UTF-8)` | **No** | Min 50 characters, Max 50,000 | Main body text of the news article |
| **`label`** | `Integer` | **No** | Must be strictly `0` (FAKE) or `1` (REAL) | Binary target classification label |
| **`source_dataset`**| `String` | **No** | Enum: `['WELFake', 'ISOT', 'LIAR']` | Name of origin dataset |
| **`scraped_date`** | `Date (ISO-8601)`| Yes | Format: `YYYY-MM-DD` | Publication or collection date |

### Null & Empty Handling Policy
1. **Missing `text` with Present `title`:** If `text` is missing or empty but `title` has $>50$ characters, `title` is copied into `text` to preserve the record.
2. **Missing Both `text` and `title`:** Record is dropped automatically during staging.
3. **Missing `label`:** Record is dropped automatically (cannot be used for supervised training).

---

## 6. Comprehensive Data Quality & Validation Checklist

```
+-----------------------------------------------------------------------------------+
|                            DATA QUALITY CHECKLIST MATRIX                          |
+-----------------------------------------------------------------------------------+
| [x] Check 1: File Existence & Format (.csv extension)                             |
| [x] Check 2: File Encoding Validation (Must be valid UTF-8 or ASCII)              |
| [x] Check 3: Cryptographic Integrity Check (SHA-256 hash match)                  |
| [x] Check 4: Schema Header Match (Required columns present)                       |
| [x] Check 5: Null Value Thresholds (Text nulls < 1.0%, Label nulls = 0.0%)        |
| [x] Check 6: Duplicate Row Detection (Zero exact full-row duplicates)             |
| [x] Check 7: Duplicate Article Text Detection (Warn on >85% text similarity)      |
| [x] Check 8: Label Domain Validation (Labels strictly in {0, 1})                  |
| [x] Check 9: Text Length Bounds (Minimum 50 characters; flags <50 as invalid)     |
| [x] Check 10: Non-Printable & Binary Character Check (Zero binary/corrupt blobs)  |
| [x] Check 11: Class Distribution Ratio (Imbalance ratio must be within 40%:60%)  |
| [x] Check 12: Publisher Shortcut Leakage Check (Flags 'Reuters' in text)          |
+-----------------------------------------------------------------------------------+
```

---

## 7. Metadata Management Strategy

Every ingestion run generates a machine-readable JSON metadata artifact in `data/metadata/` tracking provenance, integrity, and data distributions.

### Sample Metadata Schema (`data/metadata/dataset_v1.0.0.json`)

```json
{
  "metadata_version": "1.0.0",
  "dataset_name": "WELFake_Combined_News",
  "ingestion_timestamp": "2026-08-05T12:16:49Z",
  "file_info": {
    "raw_filename": "WELFake_Dataset.csv",
    "file_size_bytes": 114589234,
    "encoding": "UTF-8",
    "sha256_checksum": "a8f5f167f44f4964e6c998dee827110c904724816e8b4e72d242637f5d94e357"
  },
  "record_counts": {
    "total_rows_ingested": 72134,
    "valid_rows_retained": 71520,
    "dropped_duplicate_rows": 412,
    "dropped_null_text_rows": 202
  },
  "class_distribution": {
    "fake_count_0": 37106,
    "real_count_1": 35028,
    "imbalance_ratio": 1.059
  },
  "text_statistics": {
    "min_char_length": 52,
    "max_char_length": 48920,
    "mean_char_length": 2450.4
  },
  "provenance": {
    "source_url": "https://www.kaggle.com/datasets/saurabhshahane/fake-news-classification",
    "license": "CC0: Public Domain",
    "ingested_by": "DataEngineeringPipeline_v1.0"
  }
}
```

---

## 8. Data Versioning & Backup Policy

### Versioning Taxonomy
- **`raw_v1.0.0.csv`:** Unmodified initial raw dataset import.
- **`interim_v1.0.0.csv`:** Standardized column schema, normalized binary labels, deduplicated rows.
- **`processed_v1.0.0.csv`:** NLP clean text tokens, ready for vectorization.

### Data Security & Integrity Controls
1. **Read-Only Permissions:** `data/raw/` directory files marked with read-only file attributes (`chmod 444` on Linux/Mac, Read-Only flag on Windows) to prevent accidental mutation.
2. **Checksum Verification:** Every pipeline execution recalculates the input CSV's SHA-256 hash and compares it against `data/metadata/` logs to detect data tampering or accidental modification.
3. **Storage Exclusion:** Large `.csv` data files added to `.gitignore` to keep GitHub repository sizes lightweight, referencing remote cloud storage buckets (S3 / Render Disk) for data retrieval.

---

## 9. Data Dictionary Template

```markdown
# Dataset Data Dictionary

## Table Name: `processed_news_articles`

| Column Name | Data Type | Nullable | Primary Key | Default | Validation Rule | Description |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `article_id` | String (UUID)| NO | YES | Auto-gen | Regex UUIDv4 | Unique surrogate key for record identification |
| `title` | String | YES | NO | NULL | Length <= 500 | Headline string of the article |
| `text` | String | NO | NO | None | Length >= 50 | Full body text of the news article |
| `label` | Integer | NO | NO | None | Value IN (0, 1)| Target binary classification (0=FAKE, 1=REAL)|
| `source_dataset`| String | NO | NO | 'WELFake'| String enum | Originating benchmark dataset name |
| `scraped_date` | Date | YES | NO | NULL | ISO-8601 Date | Date when article was published/collected |
```

---

## 10. Automated Data Pipeline Script Architecture

The data pipeline consists of four modular automation scripts:

```
scripts/
├── download_dataset.py             # Downloads raw dataset archives from cloud/Kaggle API
├── validate_dataset.py             # Runs schema, encoding, null, and duplicate quality checks
├── generate_metadata.py            # Computes SHA-256 checksums and emits metadata JSON
└── generate_data_dictionary.py     # Generates markdown & HTML data dictionary docs
```

---

## 11. Error Handling & Exception Management Strategy

| Error Condition | Pipeline Behavior | Recovery Action |
| :--- | :--- | :--- |
| **Missing Raw CSV File** | Pipeline aborts immediately; raises `DataNotFoundError`. | Triggers `download_dataset.py` retry routine. |
| **Corrupted Encoding (Non-UTF8)**| Attempts fallback encoding (`cp1252`, `latin-1`). | Transcodes file to strict UTF-8 with signature strip. |
| **Checksum Mismatch** | Raises `DataIntegrityError`; halts pipeline execution. | Warns of file corruption; re-downloads original archive. |
| **Invalid Label Range (e.g. 2 or -1)**| Filters out invalid rows; logs warning count. | Quarantines malformed rows into `data/interim/quarantine.csv`. |
| **Empty File / Zero Bytes** | Raises `EmptyDatasetError`; stops downstream jobs. | Alerts developer; inspects download source. |

---

## 12. Data Engineering Implementation Roadmap

```
Phase 1: Ingestion & Storage Setup
  ├── Establish data/ directory hierarchy (raw, interim, processed, metadata)
  └── Write dataset acquisition script (scripts/download_dataset.py)
        │
Phase 2: Validation & Quality Control
  ├── Implement schema validation engine (scripts/validate_dataset.py)
  └── Execute duplicate row & label range checks
        │
Phase 3: Standardisation & Metadata Logging
  ├── Map raw headers to unified schema (article_id, title, text, label)
  └── Generate SHA-256 checksums & metadata JSON (scripts/generate_metadata.py)
        │
Phase 4: Handoff to Data Science & NLP Team
  ├── Emit verified dataset to data/processed/
  └── Generate Data Dictionary documentation & hand off to EDA team
```
