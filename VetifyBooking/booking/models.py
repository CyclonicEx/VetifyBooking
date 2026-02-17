from django.db import models
from django.contrib.auth.models import User

class Appointment(models.Model):
    PET_TYPES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('other', 'Other'),
    ]
    
    SERVICES = [
        ('checkup', 'General Checkup'),
        ('vaccination', 'Vaccination'),
        ('dental', 'Dental Cleaning'),
        ('grooming', 'Grooming'),
        ('surgery', 'Surgery Consultation'),
        ('emergency', 'Emergency Visit'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    pet_name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=10, choices=PET_TYPES, default='dog')
    owner_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    service = models.CharField(max_length=20, choices=SERVICES)
    date = models.DateField()
    time = models.TimeField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['date', 'time']
    
    def __str__(self):
        return f"{self.pet_name} - {self.date} at {self.time}"