from django.db import models
from django.conf import settings
from django.utils import timezone

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
    storage_condition = models.CharField(max_length=50, default="room_temp")
    food_type = models.CharField(max_length=50, default="cooked_meal")
    
    # Sensory ML Inputs (now persisted for retraining)
    container_type = models.CharField(max_length=50, blank=True, default="closed")
    moisture_type = models.CharField(max_length=50, blank=True, default="moist")
    cooking_method = models.CharField(max_length=50, blank=True, default="boiled")
    texture = models.CharField(max_length=50, blank=True, default="firm")
    smell = models.CharField(max_length=50, blank=True, default="neutral")
    
    # AI Results (Auto-filled)
    freshness_score = models.FloatField(null=True, blank=True)
    freshness_label = models.CharField(max_length=50, blank=True)
    confidence = models.FloatField(null=True, blank=True, help_text="ML model confidence %")
    
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    claimed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['donor']),
        ]

    def __str__(self):
        return f"{self.food_name} - {self.freshness_label} ({self.freshness_score}%)"