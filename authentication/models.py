from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False) 
    email_token = models.CharField(max_length=200, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    password_reset_token = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.username

    def delete(self, *args, **kwargs):
        
        
        super().delete(*args, **kwargs)
