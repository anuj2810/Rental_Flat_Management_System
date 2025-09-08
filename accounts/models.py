from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('owner', 'Owner'),
        ('renter', 'Renter')
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='owner')
    phone_number = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} - {self.user_type}"
    
