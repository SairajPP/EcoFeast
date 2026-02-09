from django.shortcuts import render, redirect
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView  # Added this import
from rest_framework.permissions import IsAuthenticated # Added this import
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from .serializers import UserSerializer

# ==========================================
# 1. API VIEWS (For Computer Code/Forms)
# ==========================================

class RegisterUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        # Custom logic to handle password hashing automatically
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.set_password(request.data['password']) # Hash the password!
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserProfileUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        user = request.user
        data = request.data

        # Update fields if provided
        if 'latitude' in data: user.latitude = data['latitude']
        if 'longitude' in data: user.longitude = data['longitude']
        if 'address' in data: user.address = data['address']
        
        user.save()
        return Response({"message": "Profile Updated Successfully!"}, status=status.HTTP_200_OK)

# ==========================================
# 2. FRONTEND VIEWS (For Humans/HTML Pages)
# ==========================================

def landing_view(request):
    """Renders the Home/Landing Page"""
    return render(request, 'landing.html')

def login_view(request):
    """Handles User Login"""
    if request.method == "POST":
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user:
            login(request, user)
            
            # 🟢 REDIRECT TO THE CORRECT DASHBOARD
            if user.role == 'ngo':
                return redirect('ngo-dashboard-ui')   # Goes to /api/donations/ngo-dashboard/
            elif user.role == 'donor':
                return redirect('donor-dashboard-ui') # Goes to /api/donations/donor-dashboard/
            
            return redirect('donor-dashboard-ui') # Fallback
        else:
            messages.error(request, "Invalid Credentials")
            
    return render(request, 'auth.html')

def register_view(request):
    """Renders the combined Auth page for registration"""
    return render(request, 'auth.html')

def logout_view(request):
    """Logs out the user and sends them Home"""
    logout(request)
    return redirect('landing')