import os
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from config import get_config
from src.preprocessing.text_cleaner import cleaner
from src.training.evaluate import evaluate_model
from src.utils.logger import logger

config = get_config()

def generate_starter_dataset() -> pd.DataFrame:
    """Generates a balanced dataset of news articles for initial model training."""
    fake_samples = [
        "BREAKING! Secret Alien Intelligence Uncovered in Underground Bunker! Scientists stunned as government hides truth!",
        "SHOCKING CONSPIRACY: Secret miracle potion cures all known diseases instantly! Doctors are furious and trying to ban this link!",
        "UNBELIEVABLE! Celebrity reveals secret trick to generate $10,000 per day working 5 minutes from home! Click here now!",
        "URGENT WARNING: Drinking tap water turns your brain into liquid! Secret leak exposes global agenda!",
        "BOMBSHELL REPORT: Mysterious frequency signal transmitted from moon alters human thoughts! Authorities silent!",
        "REVEALED: Secret time traveler visits 2026 and predicts instant financial collapse next week! Download report!",
        "EXPOSED: Major world leaders replaced by synthetic clones! Anonymous insider leaks confidential footage!",
        "PROOF: Hidden pyramid discovered under Antarctica ice caps contains alien technology! Media refuses to report!",
        "SHOCKING NEWS: Local man discovers formula for anti-gravity in backyard garage! NASA raiding his home!",
        "EXCLUSIVE: Secret chemical in popular soda causes immediate mind control! Destroy all bottles now!",
        "BREAKING RED ALERT: Global internet shutdown scheduled for tomorrow morning! Stock up on canned beans!",
        "STUNNING CLAIM: Scientists discover invisible dragons living in upper atmosphere! Govt coverup confirmed!",
        "LEAKED DOCUMENTS: Magic crystal energy source discovered that renders electricity bills completely obsolete!",
        "ALERT: Millions of smartphones secretly transmitting personal thoughts to offshore servers!",
        "UNBELIEVABLE DISCOVERY: Ancient map shows secret continent hidden behind wall of ice!"
    ] * 20

    real_samples = [
        "Official Government Bureau releases quarterly employment and economic growth metrics showing steady market stabilization.",
        "The Federal Reserve announced a modest interest rate adjustment following the monthly inflation data review meeting.",
        "Scientists at European research center publish peer-reviewed study on renewable solar cell efficiency advancements.",
        "Health Organization issues updated clinical guidelines for seasonal respiratory illness prevention and vaccination.",
        "Central Bank reports increased trade volume across international markets despite ongoing supply chain adjustments.",
        "Ministry of Education announces new technology funding initiative for primary and secondary public school districts.",
        "Department of Transportation completes comprehensive safety inspection across national railway infrastructure networks.",
        "Astronomers deploy space telescope array to capture high-resolution imagery of distant galaxy clusters.",
        "Agricultural agency publishes annual crop yield statistics highlighting sustainable farming practice impacts.",
        "International treaty signed by twenty nations to strengthen marine ecosystem protection and reduce ocean plastic waste.",
        "University medical research team conducts clinical trial testing efficacy of targeted immunotherapy treatments.",
        "National Weather Service issues coastal high-tide advisory following offshore low-pressure system movement.",
        "Global energy summit delegates agree on unified framework for accelerating offshore wind turbine deployment.",
        "Municipal city council approves budget allocation for urban park restoration and public transit expansion.",
        "Technology consortium releases open-source software security standards to safeguard cloud data infrastructure."
    ] * 20

    df_fake = pd.DataFrame({'text': fake_samples, 'label': 0})
    df_real = pd.DataFrame({'text': real_samples, 'label': 1})
    
    df = pd.concat([df_fake, df_real], ignore_index=True)
    df = df.sample(frac=1.0, random_state=42).reset_index(drop=True)
    return df

def train_pipeline(data_path: Path = None):
    """Executes end-to-end model training, evaluation, and serialization."""
    logger.info("Starting Machine Learning Training Pipeline...")
    
    # 1. Load Data
    if data_path and Path(data_path).exists():
        logger.info(f"Loading raw dataset from {data_path}")
        df = pd.read_csv(data_path)
    else:
        logger.info("Raw dataset not found. Generating starter benchmark dataset...")
        df = generate_starter_dataset()
        
    logger.info(f"Dataset loaded. Total samples: {len(df)} (Real: {sum(df['label']==1)}, Fake: {sum(df['label']==0)})")
    
    # 2. Text Preprocessing
    logger.info("Preprocessing text data...")
    df['clean_text'] = df['text'].apply(cleaner.clean_text)
    
    # Filter empty texts
    df = df[df['clean_text'].str.strip() != ''].reset_index(drop=True)
    
    # 3. Feature Vectorization (TF-IDF)
    logger.info("Fitting TF-IDF Vectorizer...")
    vectorizer = TfidfVectorizer(
        max_features=5000,
        ngram_range=(1, 2),
        sublinear_tf=True
    )
    X = vectorizer.fit_transform(df['clean_text'])
    y = df['label'].values
    
    # 4. Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # 5. Train Model
    logger.info("Training Logistic Regression Model...")
    model = LogisticRegression(C=1.0, max_iter=1000, random_state=42)
    model.fit(X_train, y_train)
    
    # 6. Evaluate Model
    metrics = evaluate_model(model, X_test, y_test)
    
    # 7. Save Artifacts
    config.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Saving model artifact to: {config.MODEL_PATH}")
    joblib.dump(model, config.MODEL_PATH)
    
    logger.info(f"Saving vectorizer artifact to: {config.VECTORIZER_PATH}")
    joblib.dump(vectorizer, config.VECTORIZER_PATH)
    
    logger.info("Training Pipeline Completed Successfully!")
    return metrics

if __name__ == "__main__":
    train_pipeline()
