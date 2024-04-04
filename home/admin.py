from django.contrib import admin


from .models import Room

class RoomAdmin(admin.ModelAdmin):
   
    list_display = ('room_name', 'price', 'image','availability')


admin.site.register(Room, RoomAdmin)


