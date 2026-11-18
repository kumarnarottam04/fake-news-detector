"""
High-Accuracy Machine Learning Training Pipeline for Fake News Analysis
Trains TF-IDF with PassiveAggressiveClassifier & Logistic Regression on True.csv and Fake.csv.
"""
import sys
import os
import re
import time
import json
from pathlib import Path
from multiprocessing import Pool, cpu_count

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Ensure local workspace NLTK path is registered
LOCAL_NLTK_DATA = BASE_DIR / 'data' / 'nltk_data'
import nltk
if LOCAL_NLTK_DATA.exists() and str(LOCAL_NLTK_DATA) not in nltk.data.path:
    nltk.data.path.insert(0, str(LOCAL_NLTK_DATA))

import joblib
import numpy as np
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression, PassiveAggressiveClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from config import get_config
from src.prediction.model_loader import ModelLoader
from src.utils.logger import logger

config = get_config()

# Precompile Regex patterns for high-speed preprocessing
RE_REUTERS = re.compile(r'^(?:[A-Z\s,/]+)?(?:\([A-Za-z\s]+\))?\s*[-—–]\s*', re.IGNORECASE)
RE_HTML = re.compile(r'<[^>]+>')
RE_URL = re.compile(r'https?://\S+|www\.\S+')
RE_EMAIL = re.compile(r'\S+@\S+')
RE_NON_ALPHA = re.compile(r'[^a-z\s]')
RE_MULTI_SPACES = re.compile(r'\s+')

STOP_WORDS = set(stopwords.words('english'))
LEMMATIZER = WordNetLemmatizer()


def clean_single_text(text: str) -> str:
    """Preprocesses a single text document efficiently."""
    if not isinstance(text, str) or not text:
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Strip Reuters publisher prefix (e.g., 'washington (reuters) - ')
    text = RE_REUTERS.sub('', text)
    
    # 3. Strip HTML & URLs
    text = RE_HTML.sub(' ', text)
    text = RE_URL.sub(' ', text)
    text = RE_EMAIL.sub(' ', text)
    
    # 4. Strip punctuation, numbers & special characters
    text = RE_NON_ALPHA.sub(' ', text)
    
    # 5. Tokenize, filter stopwords, and lemmatize
    tokens = text.split()
    cleaned = [
        LEMMATIZER.lemmatize(w)
        for w in tokens
        if w not in STOP_WORDS and len(w) > 2
    ]
    return " ".join(cleaned)


def clean_batch(texts):
    """Worker function for multiprocessing pool."""
    return [clean_single_text(t) for t in texts]


def parallel_clean_texts(texts_series: pd.Series, n_workers: int = None) -> list:
    """Cleans text series in parallel using all available CPU cores."""
    if n_workers is None:
        n_workers = min(cpu_count() or 4, 8)
    
    logger.info(f"Cleaning {len(texts_series)} articles in parallel using {n_workers} CPU workers...")
    t0 = time.time()
    
    # Chunk texts for worker processes
    chunk_size = max(1, len(texts_series) // (n_workers * 4))
    chunks = [texts_series.iloc[i:i + chunk_size].tolist() for i in range(0, len(texts_series), chunk_size)]
    
    with Pool(processes=n_workers) as pool:
        results = pool.map(clean_batch, chunks)
        
    cleaned_list = [item for sublist in results for item in sublist]
    elapsed = time.time() - t0
    logger.info(f"Parallel text cleaning completed in {elapsed:.2f}s ({len(cleaned_list) / elapsed:.1f} articles/s)")
    return cleaned_list


def load_and_preprocess_dataset():
    """Loads True.csv and Fake.csv, cleans text, and saves processed CSV."""
    true_csv = BASE_DIR / 'True.csv'
    fake_csv = BASE_DIR / 'Fake.csv'
    
    if not true_csv.exists() or not fake_csv.exists():
        raise FileNotFoundError(f"Missing True.csv or Fake.csv in {BASE_DIR}")
        
    logger.info("Loading True.csv and Fake.csv...")
    df_true = pd.read_csv(true_csv)
    df_fake = pd.read_csv(fake_csv)
    
    # Label: 1 for REAL, 0 for FAKE
    df_true['label'] = 1
    df_fake['label'] = 0
    
    logger.info(f"Loaded {len(df_true):,} REAL articles and {len(df_fake):,} FAKE articles.")
    
    # Combine datasets
    df = pd.concat([df_true, df_fake], ignore_index=True)
    
    # Combine Title and Text (Headlines provide critical sensationalism indicators)
    df['combined_text'] = df['title'].fillna('') + " " + df['text'].fillna('')
    
    # Drop duplicates
    initial_count = len(df)
    df = df.drop_duplicates(subset=['combined_text']).reset_index(drop=True)
    dedup_count = len(df)
    logger.info(f"Removed {initial_count - dedup_count:,} duplicate articles. Retained {dedup_count:,} unique samples.")
    
    # Clean text
    df['clean_text'] = parallel_clean_texts(df['combined_text'])
    
    # Filter empty or trivial texts
    df = df[df['clean_text'].str.strip() != ''].reset_index(drop=True)
    logger.info(f"Final valid clean articles count: {len(df):,} (Real: {sum(df['label']==1):,}, Fake: {sum(df['label']==0):,})")
    
    # Save processed dataset
    processed_dir = BASE_DIR / 'data' / 'processed'
    processed_dir.mkdir(parents=True, exist_ok=True)
    processed_file = processed_dir / 'cleaned_news.csv'
    logger.info(f"Saving cleaned dataset to {processed_file}...")
    df[['title', 'clean_text', 'label']].to_csv(processed_file, index=False)
    
    return df


def train_and_evaluate():
    """Full ML pipeline: Load -> Clean -> Vectorize -> Train -> Compare -> Save -> Connect."""
    total_start = time.time()
    
    print("\n" + "=" * 65)
    print("   FAKE NEWS ANALYSIS: MACHINE LEARNING TRAINING PIPELINE")
    print("=" * 65 + "\n")
    
    # 1. Data Cleaning
    df = load_and_preprocess_dataset()
    
    # 2. Train-Test Split (80% train, 20% test, stratified)
    print("\n[1/4] Splitting dataset (80% train, 20% test)...")
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        df['clean_text'], df['label'].values,
        test_size=0.20,
        random_state=42,
        stratify=df['label'].values
    )
    print(f"      Train samples: {len(X_train_raw):,} | Test samples: {len(X_test_raw):,}")
    
    # 3. TF-IDF Vectorization
    print("\n[2/4] Fitting TF-IDF Vectorizer (max_features=10,000, unigrams + bigrams)...")
    t0 = time.time()
    vectorizer = TfidfVectorizer(
        max_features=10000,
        ngram_range=(1, 2),
        sublinear_tf=True
    )
    X_train = vectorizer.fit_transform(X_train_raw)
    X_test = vectorizer.transform(X_test_raw)
    print(f"      TF-IDF transformation finished in {time.time() - t0:.2f}s (Vocabulary: {len(vectorizer.vocabulary_):,} features)")
    
    # 4. Train Candidate Models
    print("\n[3/4] Training and comparing candidate Machine Learning models...")
    
    candidates = {
        "PassiveAggressiveClassifier": PassiveAggressiveClassifier(
            max_iter=1000, C=0.5, random_state=42, loss='hinge'
        ),
        "LogisticRegression": LogisticRegression(
            C=2.0, max_iter=1000, random_state=42, solver='lbfgs'
        )
    }
    
    eval_results = {}
    
    for name, clf in candidates.items():
        print(f"\n      --> Training {name}...")
        t_clf = time.time()
        clf.fit(X_train, y_train)
        fit_time = time.time() - t_clf
        
        y_pred = clf.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        
        eval_results[name] = {
            "model": clf,
            "accuracy": acc,
            "precision": prec,
            "recall": rec,
            "f1_score": f1,
            "fit_time_s": round(fit_time, 2),
            "report": classification_report(y_test, y_pred, target_names=['FAKE', 'REAL'], digits=4),
            "confusion_matrix": confusion_matrix(y_test, y_pred).tolist()
        }
        
        print(f"          Accuracy : {acc * 100:.2f}%")
        print(f"          Precision: {prec * 100:.2f}%")
        print(f"          Recall   : {rec * 100:.2f}%")
        print(f"          F1-Score : {f1 * 100:.2f}%")
        print(f"          Fit time : {fit_time:.2f}s")

    # Select Best Model based on F1 / Accuracy
    best_name = max(eval_results.keys(), key=lambda k: eval_results[k]['accuracy'])
    best_info = eval_results[best_name]
    best_model = best_info['model']
    
    print("\n" + "-" * 65)
    print(f" BEST PERFORMING MODEL: {best_name} ({best_info['accuracy'] * 100:.2f}% Accuracy)")
    print("-" * 65)
    print(best_info['report'])
    
    # 5. Save Model and Vectorizer Artifacts
    print("[4/4] Saving production artifacts...")
    models_dir = BASE_DIR / 'models'
    models_dir.mkdir(parents=True, exist_ok=True)
    
    model_save_path = BASE_DIR / config.MODEL_PATH
    vectorizer_save_path = BASE_DIR / config.VECTORIZER_PATH
    
    joblib.dump(best_model, model_save_path)
    joblib.dump(vectorizer, vectorizer_save_path)
    print(f"      Model saved to      : {model_save_path}")
    print(f"      Vectorizer saved to : {vectorizer_save_path}")
    
    # Save Metadata
    metadata = {
        "trained_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "best_model_name": best_name,
        "total_samples": len(df),
        "train_samples": len(X_train_raw),
        "test_samples": len(X_test_raw),
        "accuracy": float(best_info['accuracy']),
        "precision": float(best_info['precision']),
        "recall": float(best_info['recall']),
        "f1_score": float(best_info['f1_score']),
        "confusion_matrix": best_info['confusion_matrix'],
        "candidate_comparisons": {
            k: {
                "accuracy": round(v['accuracy'] * 100, 2),
                "precision": round(v['precision'] * 100, 2),
                "recall": round(v['recall'] * 100, 2),
                "f1_score": round(v['f1_score'] * 100, 2),
                "fit_time_s": v['fit_time_s']
            } for k, v in eval_results.items()
        }
    }
    
    meta_path = models_dir / 'model_metadata.json'
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2)
    print(f"      Metadata saved to   : {meta_path}")
    
    # 6. Warm-reload into Singleton to connect directly to live app
    print("\nConnecting newly trained model to main app...")
    loader = ModelLoader()
    loader.load_artifacts(model_path=model_save_path, vectorizer_path=vectorizer_save_path, force_reload=True)
    print("Main app ModelLoader refreshed successfully with new model!")
    
    total_time = time.time() - total_start
    print(f"\nPipeline successfully completed in {total_time:.2f} seconds.")
    print("=" * 65 + "\n")
    
    return metadata


if __name__ == '__main__':
    train_and_evaluate()
