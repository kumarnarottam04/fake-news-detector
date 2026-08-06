"""
Chi-Square Feature Selector Module
"""
from sklearn.feature_selection import SelectKBest, chi2
from scipy.sparse import csr_matrix
from src.utils.logger import logger

class FeatureSelector:
    """Selects top K features based on Chi-Square statistical independence tests."""

    def __init__(self, k: int = 5000):
        self.k = k
        self.selector = SelectKBest(score_func=chi2, k=self.k)
        self.is_fitted = False

    def fit(self, X_sparse: csr_matrix, y):
        """Fits Chi-Square scores on training feature matrix."""
        logger.info(f"Fitting Chi-Square Feature Selector for Top {self.k} features...")
        self.selector.fit(X_sparse, y)
        self.is_fitted = True
        return self

    def transform(self, X_sparse: csr_matrix) -> csr_matrix:
        """Transforms sparse matrix to selected K features."""
        if not self.is_fitted:
            raise RuntimeError("FeatureSelector must be fitted before transform.")
        return self.selector.transform(X_sparse)

    def fit_transform(self, X_sparse: csr_matrix, y) -> csr_matrix:
        """Fits selector and transforms sparse matrix."""
        self.fit(X_sparse, y)
        return self.transform(X_sparse)
