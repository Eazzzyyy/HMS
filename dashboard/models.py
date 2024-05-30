from django.db import models
from home .models import Room
from authentication .models import CustomUser
from django.utils import timezone

# Create your models here.
class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)  # Foreign key relationship with Room model
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Foreign key relationship with User model
    payment_status = models.CharField(max_length=20)  # Payment status field
    check_in_date = models.DateField(default=timezone.now)  # Default value for check-in date
    check_out_date = models.DateField(default=timezone.now)  # Default value for check-out date
    price=models.IntegerField(default=0)

    # Add other fields as needed
    def __str__(self):
        return f"{self.room.room_name} - {self.user.username}"
    

class Feedback(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    feedback=models.CharField(max_length=200)
    date=models.DateField(default=timezone.now)


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.CharField(max_length=100,default='esewa')
    payment_date = models.DateField(default=timezone.now())
    amount=models.FloatField()
    transaction_uuid = models.CharField(max_length=100)
    status=models.BooleanField(default=False)



class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    review_message = models.TextField()
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    display_on_website = models.BooleanField(default=False)  # Add this field

    def __str__(self):
        return f"Review by {self.user.username} - Rating: {self.rating}"
