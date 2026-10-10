from rest_framework import generics, permissions
from .models import Donation
from .serializers import DonationSerializer
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

import os
import requests
import logging

logger = logging.getLogger(__name__)

# --- HTML VIEWS (Protected) ---
@login_required
def donor_dashboard_view(request):
    return render(request, 'donor_dashboard.html')

@login_required
def ngo_dashboard_view(request):
    return render(request, 'ngo_dashboard.html')

@login_required
def map_dashboard_view(request):
    return render(request, 'map_dashboard.html')


# --- API VIEWS ---

class CreateDonationView(generics.CreateAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data

        # Build ML input from form data
        ml_input = {
            'storage_time': float(data.get('storage_time_hours', 0) or 0),
            'time_since_cooking': float(data.get('time_since_cooking_hours', 0) or 0),
            'storage_condition': data.get('storage_condition', 'room_temperature'),
            'food_type': data.get('food_type', 'Vegetarian'),
            'container_type': data.get('container_type', 'closed'),
            'moisture_type': data.get('moisture_type', 'dry'),
            'cooking_method': data.get('cooking_method', 'boiled'),
            'texture': data.get('texture', 'firm'),
            'smell': data.get('smell', 'neutral'),
        }

        try:
            ai_host = os.environ.get('AI_SERVICE_HOST', 'localhost:8001')
            # Internal Render calls must use http, not https
            ai_url = f"http://{ai_host}"
            response = requests.post(f"{ai_url}/api/ml/predict/", json=ml_input, timeout=10)
            if response.status_code == 200:
                data = response.json()
                score = data['prediction']['freshness_score']
                label = data['prediction']['freshness_label']
                confidence = data['prediction']['confidence']
                shap_features = data.get('shap_explanation', [])
                explanation_text = "" # Adjust as needed
            else:
                logger.error(f"AI Service returned status code {response.status_code}: {response.text}")
                raise ValueError("Failed to get prediction from AI Service")
                
        except Exception as e:
            logger.error(f"ML API Error: {e}")
            score = 0
            label = "Unknown"
            confidence = None
            shap_features = []
            explanation_text = ""

        serializer.save(
            donor=self.request.user,
            freshness_score=score,
            freshness_label=label,
            confidence=confidence,
            container_type=data.get('container_type', 'closed'),
            moisture_type=data.get('moisture_type', 'dry'),
            cooking_method=data.get('cooking_method', 'boiled'),
            texture=data.get('texture', 'firm'),
            smell=data.get('smell', 'neutral'),
        )

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            response.data['freshness_score'] = response.data.get('freshness_score')
            response.data['freshness_label'] = response.data.get('freshness_label')
            response.data['confidence'] = response.data.get('confidence')
        return response


class ListDonationsView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'donor':
            return Donation.objects.filter(donor=user).order_by('-created_at')

        elif user.role in ['ngo', 'shelter']:
            return Donation.objects.filter(
                Q(status='pending') | Q(recipient=user)
            ).order_by('-created_at')

        return Donation.objects.none()


class DonationUpdateView(generics.UpdateAPIView):
    """Handles claiming donations."""
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Donation.objects.filter(status='pending')

    def perform_update(self, serializer):
        if self.request.user.role not in ['ngo', 'shelter']:
            raise permissions.PermissionDenied("Only NGOs and Shelters can claim donations.")
            
        instance = serializer.save()

        if self.request.data.get('status') == 'claimed':
            instance.recipient = self.request.user
            instance.claimed_at = timezone.now()
            instance.save()
