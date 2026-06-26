"""
Tests for GenAI Service: Vision, Chat, Explainer.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


class TestGenAIConfig:
    """Tests for GenAI configuration."""

    def test_config_import(self):
        from genai_service.config import groq_client, VISION_MODEL, TEXT_MODEL
        assert VISION_MODEL == "meta-llama/llama-4-scout-17b-16e-instruct"
        assert TEXT_MODEL == "llama-3.3-70b-versatile"
        assert groq_client is not None


class TestVisionIntake:
    """Tests for Vision Intake service."""

    def test_vision_intake_import(self):
        from genai_service.vision_intake import vision_intake
        assert vision_intake is not None

    @patch('genai_service.vision_intake.groq_client')
    def test_vision_intake_structure(self, mock_client):
        from genai_service.vision_intake import vision_intake

        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"food_name": "Test", "food_type": "Vegetarian", "quantity_kg": 5, "storage_condition": "refrigerated", "container_type": "plastic", "moisture_type": "dry", "cooking_method": "steamed", "texture": "soft", "smell": "neutral"}'))]
        mock_client.chat.completions.create.return_value = mock_response

        result = vision_intake(b"fake_image_data")

        assert 'food_name' in result
        assert 'food_type' in result
        assert 'quantity_kg' in result


class TestChatIntake:
    """Tests for Chat Intake service."""

    def test_chat_intake_import(self):
        from genai_service.chat_intake import chat_intake
        assert chat_intake is not None

    @patch('genai_service.chat_intake.groq_client')
    def test_chat_intake_structure(self, mock_client):
        from genai_service.chat_intake import chat_intake

        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='{"food_name": "Test", "food_type": "Vegetarian", "quantity_kg": 5, "storage_condition": "refrigerated", "container_type": "plastic", "moisture_type": "dry", "cooking_method": "steamed", "texture": "soft", "smell": "neutral"}'))]
        mock_client.chat.completions.create.return_value = mock_response

        result = chat_intake("I have 5kg of fresh rice")

        assert 'food_name' in result
        assert 'food_type' in result
        assert 'quantity_kg' in result


class TestExplainerLLM:
    """Tests for SHAP Explainer LLM."""

    def test_explainer_llm_import(self):
        from genai_service.explainer_llm import explain_shap
        assert explain_shap is not None

    @patch('genai_service.explainer_llm.groq_client')
    def test_explainer_llm_structure(self, mock_client):
        from genai_service.explainer_llm import explain_shap

        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content='The food is predicted fresh because it was stored in refrigerator.'))]
        mock_client.chat.completions.create.return_value = mock_response

        shap_values = {'storage_condition_refrigerated': 0.5, 'time_since_cooking_hours': -0.2}
        result = explain_shap(shap_values, 90, 'Fresh')

        assert isinstance(result, str)
        assert len(result) > 0


class TestGenAIViews:
    """Tests for GenAI API views."""

    def test_vision_intake_view_import(self):
        from genai_service.views import VisionIntakeView
        assert VisionIntakeView is not None

    def test_chat_intake_view_import(self):
        from genai_service.views import ChatIntakeView
        assert ChatIntakeView is not None

    def test_shap_explanation_view_import(self):
        from genai_service.views import SHAPExplanationView
        assert SHAPExplanationView is not None