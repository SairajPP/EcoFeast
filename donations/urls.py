from django.urls import path
from .views import (
    CreateDonationView, 
    ListDonationsView, 
    DonationUpdateView, # <--- Ensure this is imported
    donor_dashboard_view, 
    ngo_dashboard_view, 
    map_dashboard_view
)

urlpatterns = [
    # API Endpoints
    path('create/', CreateDonationView.as_view(), name='create-donation'),
    path('list/', ListDonationsView.as_view(), name='list-donations'),
    path('update/<int:pk>/', DonationUpdateView.as_view(), name='update-donation'), # <--- Check this line

    # HTML Views
    path('donor-dashboard/', donor_dashboard_view, name='donor-dashboard-ui'),
    path('ngo-dashboard/', ngo_dashboard_view, name='ngo-dashboard-ui'),
    path('map/', map_dashboard_view, name='map-dashboard'),
]