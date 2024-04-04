from django.db import models
from home .models import Room
from authentication .models import CustomUser

# Create your models here.
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Foreign key relationship with Room model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Foreign key relationship with User model
    payment_status = models.CharField(max_length=20)  # Payment status field
    # Add other fields as needed
    
    def __str__(self):
        return f"{self.room.room_name} - {self.user.username}"