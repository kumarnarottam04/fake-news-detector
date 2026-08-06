import threading
import joblib
from pathlib import Path
from config import get_config
from src.utils.logger import logger

config = get_config()

class ModelLoader:
    """Thread-safe Singleton class for warm-loading ML models into memory."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(ModelLoader, cls).__new__(cls)
                cls._instance._model = None
                cls._instance._vectorizer = None
                cls._instance._is_loaded = False
        return cls._instance

    def load_artifacts(self, model_path: Path = None, vectorizer_path: Path = None):
        """Loads serialized joblib model and vectorizer artifacts."""
        if self._is_loaded:
            return

        with self._lock:
            if self._is_loaded:
                return

            m_path = model_path or config.MODEL_PATH
            v_path = vectorizer_path or config.VECTORIZER_PATH

            if not Path(m_path).exists() or not Path(v_path).exists():
                logger.warning(f"Model artifacts missing at {m_path} / {v_path}. System requires training.")
                return False

            try:
                logger.info(f"Loading ML model artifact from: {m_path}")
                self._model = joblib.load(m_path)
                
                logger.info(f"Loading TF-IDF vectorizer artifact from: {v_path}")
                self._vectorizer = joblib.load(v_path)

                self._is_loaded = True
                logger.info("Model and vectorizer warm-loaded successfully.")
                return True
            except Exception as e:
                logger.error(f"Failed to load model artifacts: {e}", exc_info=True)
                raise e

    @property
    def model(self):
        if not self._is_loaded:
            self.load_artifacts()
        return self._model

    @property
    def vectorizer(self):
        if not self._is_loaded:
            self.load_artifacts()
        return self._vectorizer

    @property
    def is_loaded(self) -> bool:
        return self._is_loaded
