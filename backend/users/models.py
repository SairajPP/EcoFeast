from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    class UserRole(models.TextChoices):
        DONOR = 'donor', 'Donor'
        NGO = 'ngo', 'NGO'
        SHELTER = 'shelter', 'Shelter'
        RESTAURANT = 'restaurant', 'Restaurant'

    role = models.CharField(
        max_length=20, 
        choices=UserRole.choices, 
        default=UserRole.DONOR,
        help_text="The primary role of this user in the ecosystem."
    )
    
    # Contact & Profile Details
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # For NGOs/Shelters: How much food can they accept?
    capacity_kg = models.IntegerField(
        blank=True, 
        null=True, 
        help_text="Max storage capacity in KG (for Shelters/NGOs)"
    )

    # Geo-Location (For future Map features)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['role']),  # Faster filtering by role
        ]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"