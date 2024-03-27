from django.db import models


class Room(models.Model):
    room_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='room_images')
    features = models.CharField(max_length=200)
    slug=models.CharField(max_length=20,default="")
    def __str__(self):
        return self.room_name



