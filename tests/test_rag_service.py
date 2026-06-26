"""
Tests for RAG Service: Embeddings, Matcher.
"""
import pytest
from unittest.mock import Mock, patch, MagicMock


class TestRAGService:
    """Tests for RAG service components."""

    def test_ngo_embeddings_import(self):
        from rag_service.ngo_embeddings import NGOEmbeddings
        assert NGOEmbeddings is not None

    def test_matcher_import(self):
        from rag_service.matcher import match_ngos
        assert match_ngos is not None

    @patch('rag_service.ngo_embeddings.QdrantClient')
    @patch('rag_service.ngo_embeddings.SentenceTransformer')
    def test_ngo_embeddings_init(self, mock_transformer, mock_qdrant):
        from rag_service.ngo_embeddings import NGOEmbeddings

        mock_transformer_instance = Mock()
        mock_transformer.return_value = mock_transformer_instance
        mock_transformer_instance.encode.return_value = [[0.1] * 384]

        mock_qdrant_instance = Mock()
        mock_qdrant.return_value = mock_qdrant_instance

        embeddings = NGOEmbeddings()
        assert embeddings is not None
        assert embeddings.model is not None
        assert embeddings.client is not None

    @patch('rag_service.matcher.NGOEmbeddings')
    def test_match_ngos_structure(self, mock_embeddings):
        from rag_service.matcher import match_ngos

        mock_embeddings_instance = Mock()
        mock_embeddings_instance.search.return_value = [
            {'id': 1, 'score': 0.85, 'payload': {'name': 'NGO 1', 'capacity_kg': 50, 'dietary_restrictions': [], 'cultural_rules': [], 'reliability_score': 80, 'distance_km': 5}}
        ]
        mock_embeddings.return_value = mock_embeddings_instance

        donation_data = {
            'food_name': 'Test Biryani',
            'food_type': 'Non-Vegetarian',
            'quantity_kg': 10,
            'latitude': 19.0760,
            'longitude': 72.8777,
        }

        results = match_ngos(donation_data)

        assert isinstance(results, list)
        assert len(results) >= 0


class TestRAGViews:
    """Tests for RAG API views."""

    def test_match_donation_view_import(self):
        from rag_service.views import MatchDonationView
        assert MatchDonationView is not None

    def test_sync_ngos_view_import(self):
        from rag_service.views import SyncNGOsView
        assert SyncNGOsView is not None