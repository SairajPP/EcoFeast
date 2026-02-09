from django.db import models
from django.conf import settings

class Donation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CLAIMED = 'claimed', 'Claimed'
        PICKED_UP = 'picked_up', 'Picked Up'
        DELIVERED = 'delivered', 'Delivered'
        EXPIRED = 'expired', 'Expired'

    # Relationships
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="donations")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="claimed_donations")

    # Basic Info
    food_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    quantity_kg = models.FloatField()
    pickup_address = models.TextField()
    
    # ML Inputs (Critical for AI Prediction)
    storage_time_hours = models.FloatField(help_text="How long has it been stored?")
    time_since_cooking_hours = models.FloatField(help_text="Hours since preparation")
    
    # These must match the exact strings your ML model expects, or you can use choices
    storage_condition = models.CharField(max_length=50, default="room_temp") # e.g., 'refrigerated', 'outside'
    food_type = models.CharField(max_length=50, default="cooked_meal")       # e.g., 'dairy', 'bakery'
    
    # AI Results (Auto-filled)
    freshness_score = models.FloatField(null=True, blank=True)
    freshness_label = models.CharField(max_length=50, blank=True) # "Fresh", "Spoiled"
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.food_name} - {self.freshness_label} ({self.freshness_score}%)"