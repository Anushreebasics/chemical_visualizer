from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Equipment(models.Model):
    """Model for storing equipment data from CSV uploads"""
    EQUIPMENT_TYPE_CHOICES = [
        ('pump', 'Pump'),
        ('compressor', 'Compressor'),
        ('reactor', 'Reactor'),
        ('heat_exchanger', 'Heat Exchanger'),
        ('separator', 'Separator'),
        ('mixer', 'Mixer'),
        ('boiler', 'Boiler'),
        ('filter', 'Filter'),
        ('other', 'Other'),
    ]
    
    upload = models.ForeignKey('DataUpload', on_delete=models.CASCADE, related_name='equipment_items')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPE_CHOICES)
    flowrate = models.FloatField()  # in some unit (e.g., m³/h)
    pressure = models.FloatField()  # in bar or psi
    temperature = models.FloatField()  # in °C
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['equipment_type']),
            models.Index(fields=['upload']),
        ]
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"


class DataUpload(models.Model):
    """Model for tracking CSV uploads"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploads')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_records = models.IntegerField(default=0)
    avg_flowrate = models.FloatField(default=0.0)
    avg_pressure = models.FloatField(default=0.0)
    avg_temperature = models.FloatField(default=0.0)
    
    class Meta:
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['user', 'uploaded_at']),
        ]
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"


class UserProfile(models.Model):
    """Extended user profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
