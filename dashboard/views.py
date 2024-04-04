import re
from django.shortcuts import redirect, render
from authentication.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Booking
from home . models import Room
from django.utils import timezone
@login_required
def UserBookings(request):
     return render(request, 'dashboard/user-bookings.html')

@login_required
def Payment(request):
     return render(request, 'dashboard/payment.html')

@login_required
def ReviewRating(request):
         return render(request, 'dashboard/reviews-rating.html')





@login_required
def Profile(request):
    user_profile = CustomUser.objects.get(username=request.user.username)

    if request.method == 'POST':
        # Extract JSON data from request body
        data = json.loads(request.body)
        
        # Extract firstname, lastname, and contact number from JSON data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        contact_number = data.get('contact_number')

        # Validation
        errors = {}

        if len(str(contact_number)) != 10:
            errors['contact'] = "The contact number should be exactly 10 digits."

        if CustomUser.objects.exclude(username=user_profile.username).filter(contact_number=contact_number).exists():
            errors['contact'] = "The contact number is already in use. Please choose a different contact number."
        
        if 'contact' in errors:
            # If there are errors, return the errors as JSON response
            return JsonResponse(errors)
        else:
            # Update user information
            user_profile.first_name = first_name
            user_profile.last_name = last_name
            user_profile.contact_number = contact_number

            # Save the updated user object
            user_profile.save()
          
            # Return success message as JSON response
            return JsonResponse({'success': "Saved successfully!"})

    # Pass the profile data to the template
    return render(request, 'dashboard/profile.html', {'user_profile': user_profile})


def AdminDashboard(request):
      return render(request, 'dashboard/admin-dashboard.html')

def Staffs(request):
    staff_members = CustomUser.objects.filter(is_staff=True,is_verified=True)
    context = {
        'staff_members': staff_members
    }
    return render(request, 'dashboard/staffs.html', context)


def CreateStaff(request):
    context = {
        'username': '',
        'fname': '',
        'lname': '',
        'contact': '',
        'pass1': '',
        'errors': {}  # Initialize empty dictionary for error messages
    }

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        contact = request.POST['contact']
        pass1 = request.POST['pass1']

        context = {
            'username': username,
            'fname': fname,
            'lname': lname,
        
            'contact': contact,
            'pass1': pass1,
            
            'errors': {}  # Reset errors dictionary for each request
        }

        status = False

        if CustomUser.objects.filter(username=username).exists():
            context['errors']['username'] = "Username is already in use. Please choose a different username."
            status = True
      
      

        if len(username) > 15:
            context['errors']['username'] = "The username cannot be longer than 15 characters."
            status = True

       

        alphanumeric_pattern = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

        if not alphanumeric_pattern.match(username):
            context['errors']['username'] = "The username must be alphanumeric and contain at least 8 characters."
            status = True

        if not alphanumeric_pattern.match(pass1):
            context['errors']['pass1'] = "The password must be alphanumeric and contain at least 8 characters."
            status = True

        if CustomUser.objects.filter(contact_number=contact).exists():
            context['errors']['contact'] = "The contact number is already in use. Please choose a different contact number."
            status = True

        if len(str(contact)) != 10:
            context['errors']['contact'] = "The contact number should be exactly 10 digits."
            status = True

        if status:
            return render(request, 'dashboard/create-staff.html',context)

        
        my_user = CustomUser.objects.create_user(username, "staff@gmail.com", pass1)
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.contact_number = contact
        my_user.is_staff=True
        my_user.is_verified=True
        
        my_user.save()
        context={
            'status':True
        }
        messages.success(request, "Created Successfully")
        return redirect('staffs')

    return render(request, 'dashboard/create-staff.html',context)



@csrf_exempt
def EditStaff(request, id):
    staff_member = CustomUser.objects.get(pk=id)

    if request.method == "POST":
        # Retrieve JSON data from the request body
        data = json.loads(request.body)

        new_contact = data.get('contact')
        errors = {}

        # Validate contact number
        if new_contact and new_contact != staff_member.contact_number:
            if CustomUser.objects.filter(contact_number=new_contact).exists():
                errors['contact'] = "The contact number is already in use. Please choose a different contact number."
            elif len(str(new_contact)) != 10:
                errors['contact'] = "The contact number should be exactly 10 digits."

        # Check for validation errors
        if errors:
            return JsonResponse(errors)

        # Update staff member details if no errors
        staff_member.first_name = data.get('first_name')
        staff_member.last_name = data.get('last_name')
        staff_member.contact_number = new_contact
        staff_member.save()

        # Return success message as JSON response
        return JsonResponse({'success': "Saved successfully!"})

    else:
        context = {'staff_member': staff_member}
        return render(request, 'dashboard/edit-staff.html', context)



    
    
@csrf_exempt  
def DeleteStaff(request,id):
    
    try:
        user = CustomUser.objects.get(id=id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def admin_reviews_ratings(request):
    return render(request,'dashboard/admin-reviews-ratings.html')

def Rooms(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'dashboard/rooms.html',context)


def CreateRoom(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        availability=request.POST.get('availability')
        price = request.POST.get('price')
        image = request.FILES.get('image')
        features_string = request.POST.get('features-string')
        print(features_string)

        # Save Room object with extracted data
        room = Room(room_name=room_name, availability=availability,price=price, image=image, features=features_string, slug='')
        room.save()
       

        return render(request, 'dashboard/create-room.html') 
    else:
        return render(request, 'dashboard/create-room.html')
    


    
def EditRoom(request, id):
    if request.method == "POST":
        room = Room.objects.get(id=id)
        room.room_name = request.POST.get('room_name')
        room.availability=request.POST.get('availability')
        room.price = request.POST.get('price')
        room.features = request.POST.get('features-string')
        
        # Check if a new image was uploaded
        new_image = request.FILES.get('new_image')
        if new_image:
            room.image = new_image

        room.save()
        messages.success(request,'Saved successfully!')
        return redirect('rooms')  # Redirect to the rooms page
    else:
        # Retrieve room and render edit page
        room = Room.objects.get(id=id)
        features_string = room.features
        features_list = features_string.split(', ')
        features = [feature.split(' ')[1] for feature in features_list]
        counts = [int(feature.split(' ')[0]) if feature.split(' ')[0] else 0 for feature in features_list]
        features_counts = zip(features, counts)

        context = {
            'room': room,
            'features_counts': features_counts,
        }
        return render(request, 'dashboard/edit-room.html', context)


    

@csrf_exempt  
def DeleteRoom(request,id):
    
    try:
        user = Room.objects.get(id=id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def BookRoom(request, id):
    # Retrieve the room object using the slug
    room = Room.objects.get(id=id)
    print(request.user.id)
    if request.method == 'POST':
        # Retrieve room ID from the POST request
        room_id = id

        # Save the booking data to the Booking model
        booking = Booking.objects.create(user=request.user,room_id=int(room_id),payment_status=False)

        # Return a JSON response indicating success
        return JsonResponse({'message': 'Booking successful'})

    # Return an error response if the request method is not POST
    

    return render(request, 'dashboard/book-room.html', {'room': room})