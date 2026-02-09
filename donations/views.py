from rest_framework import generics, permissions
from .models import Donation
from .serializers import DonationSerializer
from ml_service.predictor import FreshnessPredictor
from django.shortcuts import render
from django.db.models import Q  # Needed for complex queries

# --- HTML VIEWS ---
def donor_dashboard_view(request):
    return render(request, 'donor_dashboard.html')

def ngo_dashboard_view(request):
    return render(request, 'ngo_dashboard.html')

def map_dashboard_view(request):
    return render(request, 'map_dashboard.html')


# --- API VIEWS ---

class CreateDonationView(generics.CreateAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        data = self.request.data
        
        # 1. Get the real-time temperature from the frontend
        # Default to 25°C if something goes wrong
        real_temp = float(data.get('current_temperature', 25))

        # 2. Prepare ML Input
        ml_input = {
            'storage_time': float(data.get('storage_time_hours', 0) or 0),
            'time_since_cooking': float(data.get('time_since_cooking_hours', 0) or 0),
            'storage_condition': data.get('storage_condition', 'outside'),
            'food_type': data.get('food_type', 'Vegetarian'), 
            'temperature': real_temp,  
            'container_type': 'plastic', 
            'moisture_type': 'dry',
            'cooking_method': 'fried',
            'texture': 'soft',
            'smell': 'neutral'
        }

        # 3. Call AI Service
        try:
            prediction = FreshnessPredictor.predict(ml_input)
            score = prediction['freshness_score']
            label = prediction['freshness_label']
        except Exception as e:
            print(f"ML Error: {e}")
            score = 0
            label = "Unknown"

        serializer.save(
            donor=self.request.user,
            freshness_score=score,
            freshness_label=label
        )


class ListDonationsView(generics.ListAPIView):
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # 1. DONORS: See ALL their own history
        if user.role == 'donor':
            return Donation.objects.filter(donor=user).order_by('-created_at')
        
        # 2. NGOs: See 'Pending' OR 'Claimed by ME' (Using 'recipient')
        elif user.role in ['ngo', 'shelter']:
            return Donation.objects.filter(
                Q(status='pending') | Q(recipient=user)  # <--- FIXED: using recipient
            ).order_by('-created_at')
            
        return Donation.objects.none()


class DonationUpdateView(generics.UpdateAPIView):
    """
    Handles claiming donations.
    """
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # Save the update
        instance = serializer.save()
        
        # If status is changing to 'claimed', verify WHO claimed it
        if self.request.data.get('status') == 'claimed':
            instance.recipient = self.request.user  # <--- FIXED: using recipient
            instance.save()