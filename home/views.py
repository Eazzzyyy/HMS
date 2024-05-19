from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse

from dashboard.models import Review
from .models import Room
from django.contrib.auth import logout
from django.shortcuts import redirect

def Homepage(request):
   rooms = Room.objects.all()
   count={}
   i=0
   
   
   return render(request,'home/homepage.html',{'rooms':rooms })


def check_login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'logged_in': True,'user':request.user.username})
    else:
        return JsonResponse({'logged_in': False})
    


def logout_view(request):
    logout(request)
    return redirect('home')

import json
def room_available(request):
    bookings = request.GET.get('bookings')  # Get the bookings data from query parameters
    status = request.GET.get('status')  # Get the status from query parameters
    bookings = json.loads(bookings)  # Convert JSON string to Python dictionary

    available_rooms = []
    # Iterate through the bookings and fetch available rooms
    for room_name, room_count in bookings.items():
        # Fetch rooms based on room_name and availability criteria
      
        rooms = Room.objects.filter(room_name=room_name)
        # Extend each room object with the room_count
        for room in rooms:
            room.room_count = room_count
        available_rooms.extend(rooms)

    # Render the template with the available rooms and room counts
    return render(request, 'home/available_rooms.html', {'available_rooms': available_rooms})

from django.http import JsonResponse
from django.db.models import Sum
from .models import Room
from authentication.models import CustomUser

def total_max_rooms(request):
    total_max = Room.objects.aggregate(total_max_rooms=Sum('max_room'))['total_max_rooms']
    staff_members = CustomUser.objects.filter(is_staff=True,is_verified=True).values('id', 'username', 'email', 'contact_number')
    reviews=Review.objects.count()
    print(list(staff_members))
    return JsonResponse({'total_max_rooms': total_max,'total_staff':len(list(staff_members)), 'reviews':reviews})

from django.http import JsonResponse
from .models import Room

def get_room_price(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        return JsonResponse({'price': room.price})
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
