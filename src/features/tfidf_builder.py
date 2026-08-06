"""
TF-IDF Feature Builder & Vectorizer Wrapper
"""
from typing import List
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from src.features.config import VectorizerConfig
from src.utils.logger import logger

class TFIDFFeatureBuilder:
    """Production-Grade TF-IDF Feature Engineering Builder."""

    def __init__(self, config: VectorizerConfig = None):
        self.config = config or VectorizerConfig()
        self.vectorizer = TfidfVectorizer(
            max_features=self.config.max_features,
            min_df=self.config.min_df,
            max_df=self.config.max_df,
            ngram_range=self.config.ngram_range,
            sublinear_tf=self.config.sublinear_tf,
            use_idf=self.config.use_idf,
            smooth_idf=self.config.smooth_idf,
            norm=self.config.norm
        )
        self.is_fitted = False

    def fit(self, raw_documents: List[str]):
        """Fits the TF-IDF vocabulary and IDF weights exclusively on training documents."""
        logger.info(f"Fitting TF-IDF Vectorizer on {len(raw_documents)} documents...")
        self.vectorizer.fit(raw_documents)
        self.is_fitted = True
        logger.info(f"Vectorizer fitted. Vocabulary size: {len(self.vectorizer.vocabulary_)} terms.")
        return self

    def transform(self, raw_documents: List[str]) -> csr_matrix:
        """Transforms documents into sparse CSR matrix using frozen vocabulary."""
        if not self.is_fitted:
            raise RuntimeError("Vectorizer must be fitted before calling transform().")
        return self.vectorizer.transform(raw_documents)

    def fit_transform(self, raw_documents: List[str]) -> csr_matrix:
        """Fits vocabulary and transforms training documents in one step."""
        self.fit(raw_documents)
        return self.transform(raw_documents)

    def get_feature_names(self) -> List[str]:
        """Returns list of feature names corresponding to matrix column indices."""
        if not self.is_fitted:
            raise RuntimeError("Vectorizer must be fitted before retrieving feature names.")
        return self.vectorizer.get_feature_names_out().tolist()
