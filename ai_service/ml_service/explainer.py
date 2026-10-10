"""
SHAP-based model explainability.
Returns top contributing features for each prediction.
"""

import os
import logging
import numpy as np
import xgboost as xgb
import joblib
from typing import Dict, List, Optional
from .feature_builder import FeatureBuilder

logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'freshness_xgb_v1.json')
ENCODER_PATH = os.path.join(BASE_DIR, 'models', 'feature_builder_v1.pkl')

class FreshnessExplainer:
    def __init__(self):
        self.model: Optional[xgb.XGBClassifier] = None
        self.feature_builder: Optional[FeatureBuilder] = None
        self._loaded = False
        self._load()

    def _load(self):
        if not os.path.exists(MODEL_PATH):
            return

        try:
            self.model = xgb.XGBClassifier()
            self.model.load_model(MODEL_PATH)

            if os.path.exists(ENCODER_PATH):
                self.feature_builder = joblib.load(ENCODER_PATH)

            self._loaded = True
        except Exception as e:
            logger.error(f"Failed to load explainer: {e}")

    def explain(self, input_data: Dict, top_n: int = 3) -> List[Dict]:
        # SHAP disabled to save RAM on Render Free Tier
        return []

    def explain_to_text(self, input_data: Dict) -> str:
        return "Explanation unavailable (Memory Optimized Mode)."

    @property
    def is_loaded(self) -> bool:
        return self._loaded


# Singleton
_explainer_instance: Optional[FreshnessExplainer] = None


def get_explainer() -> FreshnessExplainer:
    global _explainer_instance
    if _explainer_instance is None or not _explainer_instance.is_loaded:
        _explainer_instance = FreshnessExplainer()
    return _explainer_instance
