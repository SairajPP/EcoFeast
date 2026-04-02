from rest_framework import generics, permissions
from .models import Donation
from .serializers import DonationSerializer
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from .ml_service import FoodQualityPredictor 

# Initialize AI once (Global Scope)
predictor = FoodQualityPredictor()

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
        
        real_temp = float(data.get('current_temperature', 25))

        ml_input = {
            'storage_time': float(data.get('storage_time_hours', 0) or 0),
            'time_since_cooking': float(data.get('time_since_cooking_hours', 0) or 0),
            'storage_condition': data.get('storage_condition', 'outside'),
            'food_type': data.get('food_type', 'Vegetarian'), 
            'temperature': real_temp,
            'city': data.get('city', 'Mumbai'),
            'container_type': data.get('container_type', 'closed'), 
            'moisture_type': data.get('moisture_type', 'moist'),
            'cooking_method': data.get('cooking_method', 'boiled'),
            'texture': data.get('texture', 'firm'),
            'smell': data.get('smell', 'neutral')
        }

        try:
            prediction = predictor.predict(ml_input)
            
            score = prediction['freshness_score']
            label = prediction['freshness_label']
            confidence = prediction.get('confidence', None)

        except Exception as e:
            print(f"⚠️ ML Error: {e}")
            score = 0
            label = "Unknown"
            confidence = None

        serializer.save(
            donor=self.request.user,
            freshness_score=score,
            freshness_label=label,
            confidence=confidence,
            container_type=data.get('container_type', 'closed'),
            moisture_type=data.get('moisture_type', 'moist'),
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
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        instance = serializer.save()
        
        if self.request.data.get('status') == 'claimed':
            instance.recipient = self.request.user
            instance.claimed_at = timezone.now()
            instance.save()