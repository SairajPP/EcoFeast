"""
Tests for ML Service: FeatureBuilder, Predictor, Explainer.
"""
import pytest
import numpy as np


class TestFeatureBuilder:
    """Tests for FeatureBuilder class."""

    def test_feature_builder_import(self):
        from ml_service.feature_builder import FeatureBuilder
        assert FeatureBuilder is not None

    def test_feature_builder_initialization(self):
        from ml_service.feature_builder import FeatureBuilder
        fb = FeatureBuilder()
        assert fb is not None
        assert hasattr(fb, 'feature_names')
        assert len(fb.feature_names) > 0

    def test_feature_builder_fit_transform(self):
        from ml_service.feature_builder import FeatureBuilder
        import pandas as pd

        fb = FeatureBuilder()
        sample_data = pd.DataFrame([{
            'food_type': 'Vegetarian',
            'storage_condition': 'refrigerated',
            'container_type': 'plastic',
            'moisture_type': 'dry',
            'cooking_method': 'steamed',
            'texture': 'soft',
            'smell': 'neutral',
            'storage_time_hours': 4,
            'time_since_cooking_hours': 2,
            'quantity_kg': 5,
        }])

        X = fb.fit_transform(sample_data)
        assert X.shape[0] == 1
        assert X.shape[1] == len(fb.feature_names)

    def test_feature_builder_transform_consistency(self):
        from ml_service.feature_builder import FeatureBuilder
        import pandas as pd

        fb = FeatureBuilder()
        sample_data = pd.DataFrame([{
            'food_type': 'Non-Vegetarian',
            'storage_condition': 'room_temp',
            'container_type': 'metal',
            'moisture_type': 'wet',
            'cooking_method': 'fried',
            'texture': 'firm',
            'smell': 'strong',
            'storage_time_hours': 6,
            'time_since_cooking_hours': 3,
            'quantity_kg': 10,
        }])

        fb.fit(sample_data)
        X1 = fb.transform(sample_data)
        X2 = fb.transform(sample_data)
        np.testing.assert_array_equal(X1, X2)

    def test_feature_builder_feature_names(self):
        from ml_service.feature_builder import FeatureBuilder
        fb = FeatureBuilder()
        names = fb.get_feature_names()
        assert isinstance(names, list)
        assert len(names) > 0
        assert all(isinstance(n, str) for n in names)


class TestPredictor:
    """Tests for Predictor class."""

    def test_predictor_import(self):
        from ml_service.predictor import Predictor
        assert Predictor is not None

    def test_predictor_singleton(self):
        from ml_service.predictor import Predictor
        p1 = Predictor()
        p2 = Predictor()
        assert p1 is p2

    def test_predictor_load_model(self):
        from ml_service.predictor import Predictor
        predictor = Predictor()
        assert predictor.model is not None
        assert predictor.feature_builder is not None

    def test_predictor_predict(self):
        from ml_service.predictor import Predictor
        predictor = Predictor()

        result = predictor.predict({
            'food_type': 'Vegetarian',
            'storage_condition': 'refrigerated',
            'container_type': 'plastic',
            'moisture_type': 'dry',
            'cooking_method': 'steamed',
            'texture': 'soft',
            'smell': 'neutral',
            'storage_time_hours': 4,
            'time_since_cooking_hours': 2,
            'quantity_kg': 5,
        })

        assert 'freshness_score' in result
        assert 'freshness_label' in result
        assert 'confidence' in result
        assert 0 <= result['freshness_score'] <= 100
        assert result['freshness_label'] in ['Fresh', 'Medium', 'Low']
        assert 0 <= result['confidence'] <= 100

    def test_predictor_predict_proba(self):
        from ml_service.predictor import Predictor
        predictor = Predictor()

        probas = predictor.predict_proba({
            'food_type': 'Vegetarian',
            'storage_condition': 'refrigerated',
            'container_type': 'plastic',
            'moisture_type': 'dry',
            'cooking_method': 'steamed',
            'texture': 'soft',
            'smell': 'neutral',
            'storage_time_hours': 4,
            'time_since_cooking_hours': 2,
            'quantity_kg': 5,
        })

        assert len(probas) == 3  # 3 classes
        assert abs(sum(probas) - 1.0) < 0.01


class TestExplainer:
    """Tests for SHAP Explainer."""

    def test_explainer_import(self):
        from ml_service.explainer import Explainer
        assert Explainer is not None

    def test_explainer_explain(self):
        from ml_service.explainer import Explainer
        from ml_service.predictor import Predictor

        predictor = Predictor()
        explainer = Explainer(predictor.model, predictor.feature_builder)

        shap_values = explainer.explain({
            'food_type': 'Vegetarian',
            'storage_condition': 'refrigerated',
            'container_type': 'plastic',
            'moisture_type': 'dry',
            'cooking_method': 'steamed',
            'texture': 'soft',
            'smell': 'neutral',
            'storage_time_hours': 4,
            'time_since_cooking_hours': 2,
            'quantity_kg': 5,
        })

        assert isinstance(shap_values, dict)
        assert len(shap_values) > 0