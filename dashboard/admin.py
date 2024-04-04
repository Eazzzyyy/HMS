from django.contrib import admin




from .models import Booking

class BookingAdmin(admin.ModelAdmin):
   
    list_display = ('id',)


admin.site.register(Booking, BookingAdmin)