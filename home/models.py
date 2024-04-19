from django.db import models
from django.utils.text import slugify

class Room(models.Model):
    room_name = models.CharField(max_length=100)
    price = models.CharField(max_length=10)
    image = models.ImageField(upload_to='room_images')
    features = models.CharField(max_length=200)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    availability = models.IntegerField(default=0)
    max_room=models.IntegerField(default=5)
    number_of_adult=models.IntegerField(default=0)
    number_of_children=models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        if not self.slug:  # Generate slug only if it's not provided
            self.slug = slugify(self.room_name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.room_name
