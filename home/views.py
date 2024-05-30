import json
from django.http import JsonResponse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render
from django.db.models import Avg, Count
from dashboard.models import Review, Room
from home.models import Room 
from django.db.models import Sum
from authentication.models import CustomUser


# def Homepage(request):
#     rooms = Room.objects.all()  # Retrieve all rooms
    
#     room_ratings = []
#     for room in rooms:  # Iterate over each room
#         # Filter reviews for the current room based on bookings associated with the room
#         reviews = Review.objects.filter(booking__room=room).aggregate(
#             average_rating=Avg('rating'), 
#             review_count=Count('id')
#         )
        
#         # Append a dictionary with room details and its ratings to the list
#         room_ratings.append({
#             'room': room,
#             'average_rating': reviews['average_rating'] if reviews['average_rating'] else 0,
#             'review_count': reviews['review_count']
#         })

#     # Get reviews to display on the homepage
#     reviews = Review.objects.filter(display_on_website=True)

#     # Pass the list of room ratings and reviews to the context
#     context = {
#         'room_ratings': room_ratings,
#         'reviews': reviews
#     }
    
#     return render(request, 'home/homepage.html', context)


def Homepage(request):
    rooms = Room.objects.all()  # Retrieve all rooms
    
    room_ratings = []
    for room in rooms:  # Iterate over each room
        # Filter reviews for the current room based on bookings associated with the room
        reviews = Review.objects.filter(booking__room=room).aggregate(
            average_rating=Avg('rating'), 
            review_count=Count('id')
        )
        
        # Append a dictionary with room details and its ratings to the list
        room_ratings.append({
            'room': room,
            'average_rating': reviews['average_rating'] if reviews['average_rating'] else 0,
            'review_count': reviews['review_count'],
            'number_of_adult': room.number_of_adult,
            'number_of_children': room.number_of_children,
        })

    # Get reviews to display on the homepage
    reviews = Review.objects.filter(display_on_website=True)

    # Pass the list of room ratings and reviews to the context
    context = {
        'room_ratings': room_ratings,
        'reviews': reviews
    }
    
    return render(request, 'home/homepage.html', context)




def check_login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'logged_in': True,'user':request.user.username})
    else:
        return JsonResponse({'logged_in': False})
    


def logout_view(request):
    logout(request)
    return redirect('home')



def room_available(request):
    bookings = request.GET.get('bookings')  # Get the bookings data from query parameters
    status = request.GET.get('status')  # Get the status from query parameters
    bookings = json.loads(bookings)  # Convert JSON string to Python dictionary

    available_rooms = []
    for room_name, room_count in bookings.items():
        rooms = Room.objects.filter(room_name=room_name)
        for room in rooms:
            reviews = Review.objects.filter(booking__room=room).aggregate(
                average_rating=Avg('rating'), 
                review_count=Count('id')
            )
            room.room_count = room_count
            room.average_rating = reviews['average_rating'] if reviews['average_rating'] else 0
          
            room.review_count = reviews['review_count']
            available_rooms.append(room)

    return render(request, 'home/available_rooms.html', {'available_rooms': available_rooms})



def total_max_rooms(request):
    total_max = Room.objects.aggregate(total_max_rooms=Sum('max_room'))['total_max_rooms']
    staff_members = CustomUser.objects.filter(is_staff=True,is_verified=True).values('id', 'username', 'email', 'contact_number')
    reviews=Review.objects.count()
    print(list(staff_members))
    return JsonResponse({'total_max_rooms': total_max,'total_staff':len(list(staff_members)), 'reviews':reviews})



def get_room_price(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
        return JsonResponse({'price': room.price})
    except Room.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
