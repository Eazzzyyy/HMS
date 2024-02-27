
# Register your models here.


from django.contrib import admin
from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'contact_number','is_staff','is_verified')

    exclude=['password','email_token']
admin.site.register(CustomUser, CustomUserAdmin)
