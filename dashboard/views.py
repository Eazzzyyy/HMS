import re
from django.shortcuts import get_object_or_404, redirect, render
from authentication.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dashboard.models import Booking
from home . models import Room
from datetime import datetime
from django.utils import timezone
from django.db.models import Q
from .utils import admin_required, send_booking_email, send_confirmation_email, send_extension_error,user_required,staff_required, send_extension
from . models import  Review
from threading import Thread
from .models import Feedback
from django.db.models import Sum
from django.http import JsonResponse
from django.views.decorators.http import require_GET
import base64
import json
import hashlib
import hmac
import base64



@user_required
def UserBookings(request):
    # Retrieve all bookings associated with the current user
    bookings = Booking.objects.filter(user=request.user)
    
    # Pass the bookings queryset to the template context
    context = {
        'bookings': bookings
    }
    
    # Render the template with the bookings data
    return render(request, 'dashboard/user-bookings.html', context)

@user_required
def Payment(request):
    bookings = Booking.objects.filter(user=request.user, payment_status="Paid")
    
    # Pass the bookings queryset to the template context
    context = {
        'bookings': bookings
    }
     
     
    return render(request, 'dashboard/payment.html',context)

@user_required
def ReviewRating(request,id):
    if request.method == 'POST':
        review_message = request.POST.get('review_message')
        rating = request.POST.get('rating')
        user = request.user
        booking = get_object_or_404(Booking, id=id)

        if review_message and rating:
            # Check if the review already exists
            review, created = Review.objects.update_or_create(
                user=user,
                booking=booking,
                defaults={'review_message': review_message, 'rating': int(rating)}
            )
            if created:
                return JsonResponse({'success': True, 'message': 'Your review has been submitted successfully!'})
            else:
                return JsonResponse({'success': True, 'message': 'Your review has been updated successfully!'})
        
        return JsonResponse({'success': False, 'message': 'Please fill in all fields.'})
    
       
    return render(request, 'dashboard/reviews-rating.html')





@staff_required
def StaffProfile(request):
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
   
     return render(request, 'dashboard/staff-profile.html')

@staff_required
def StaffBookRoom(request):
    return render(request, 'dashboard/staff-book-room.html')






@user_required
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
    return render(request, 'dashboard/profile.html', {'user_profile': user_profile,'username':request.user.username})

@login_required
@admin_required
def AdminDashboard(request):
      return render(request, 'dashboard/admin-dashboard.html')


@staff_required
def StaffDashboard(request):
    bookings = Booking.objects.all()
    all_users = CustomUser.objects.filter(is_staff=False, is_superuser=False)
    context = {
            'bookings': bookings,
            'all_users': all_users
        }
    return render(request, 'dashboard/staff-dashboard.html', context)

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
    
@csrf_exempt  
def DeleteFeedback(request,id):
    
   
        feedback= Feedback.objects.get(id=id)
        feedback.delete()
        
        return JsonResponse({'message': 'Feedback deleted successfully'}, status=200)
    

    
def admin_reviews_ratings(request):
    reviews = Review.objects.all()
    context={

        'reviews': reviews
    }
    return render(request,'dashboard/admin-reviews-ratings.html',context)

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
        adults=request.POST.get('adults')
        children=request.POST.get('children')
        print(features_string)

        # Save Room object with extracted data
        room = Room(room_name=room_name, availability=availability,price=price, image=image, features=features_string,max_room=availability,number_of_adult=adults,number_of_children=children)
        room.save()
       

        return render(request, 'dashboard/create-room.html') 
    else:
        return render(request, 'dashboard/create-room.html')
    


    
def EditRoom(request, id):
    if request.method == "POST":
        room = Room.objects.get(id=id)
        room.room_name = request.POST.get('room_name')
        room.availability=request.POST.get('availability')
        room.max_room=request.POST.get('availability')
        room.price = request.POST.get('price')
        room.features = request.POST.get('features-string')
        room.number_of_adult=request.POST.get('adults')
        room.number_of_children=request.POST.get('children')

        
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
        return JsonResponse({'message': 'Room deleted successfully'}, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

@csrf_exempt  
def DeleteBooking(request,id):
    try:
        user = Booking.objects.get(id=id)
        user.delete()
        return JsonResponse({'message': 'Room deleted successfully'}, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    


def EditBooking(request,id):
    if request.method == 'POST':
        id = request.POST.get('id')
        status = request.POST.get("payment_status")
        booking = Booking.objects.get(id=id)
        booking.payment_status = status
        booking.save()

        return JsonResponse({'success': 'Payment status updated successfully'})

    context = {
        'booking': Booking.objects.get(id=id)
    }
    return render(request, 'dashboard/edit-booking.html', context)








def send_booking_email_thread(email):
    send_booking_email(email)



def BookRoom(request, id):
    room = Room.objects.get(id=id)
    
    if request.method == 'POST':
        json_data = json.loads(request.body)

        room_id = json_data.get('room_id')
        checkin_str = json_data.get('checkin')
        checkout_str = json_data.get('checkout')
        price = json_data.get('price')
        book_status = json_data.get('book_status', 0)
        checkin_date = datetime.strptime(checkin_str, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout_str, '%Y-%m-%d').date()

        if not Booking.objects.filter(room_id=room_id, check_out_date__lte=checkin_date).exists():
            if Booking.objects.filter(room_id=room_id, check_out_date__gte=checkin_date).exists():
                if Room.objects.filter(id=room_id, availability=0):
                    return JsonResponse({'message': 'Room already booked'})

        booking = Booking.objects.create(
            user=request.user,
            room_id=int(room_id),
            check_in_date=checkin_date,
            check_out_date=checkout_date,
            payment_status="Pending",
            price=price,
        )

        room.save()

        # Send JSON response immediately
        response = JsonResponse({'message': 'Booking successful. You will receive a confirmation email shortly.'})

        # Send the booking email in a separate thread
        if not book_status:
            Thread(target=send_booking_email_thread, args=(request.user.email,)).start()

        return response

    room = Room.objects.get(id=id)
    reviews = Review.objects.filter(booking__room__id=id)
    return render(request, 'dashboard/book-room.html', {'room': room, 'reviews': reviews})



 
def booking_list(request, roomname):
   
    checkin_date= request.GET.get("check_in_date")
    checkout_date=request.GET.get("check_out_date")
    checkin_date = timezone.datetime.strptime(checkin_date, '%Y-%m-%d').date()
    checkout_date = timezone.datetime.strptime(checkout_date, '%Y-%m-%d').date()

    if checkin_date == checkout_date:
        return JsonResponse({'message': 'Checkin date and Checkout date cannot be the same',"status":2})

    if checkout_date < checkin_date:
        
        return JsonResponse({'message': 'Checkout date should be after the Checkin date',"status":2})
    

    user = request.user

    # Retrieve all bookings for the logged-in user
    bookings = Booking.objects.filter(  Q(check_in_date=checkin_date, check_out_date=checkout_date,user=user,room__room_name=roomname) ).exists()

    # Check if each booking has a checkout date after today
    

    if bookings:
           return JsonResponse({'message': "Cannot book the same room twice","status":2})

    bookings = Booking.objects.filter(
        Q(check_in_date__lt=checkout_date, check_out_date__gt=checkin_date,room__room_name=roomname) |
        Q(check_in_date__gte=checkin_date, check_out_date__lte=checkout_date,room__room_name=roomname) |
        Q(check_in_date__lt=checkin_date, check_out_date__gt=checkout_date,room__room_name=roomname)
    )
    
   
    room=Room.objects.get(room_name=roomname)
    
    latest_booking=0
    if bookings:
        bookings = bookings.order_by('check_out_date')
        # Get the latest booking (first booking in the ordered queryset)
        latest_booking = bookings.first()
    
    # Convert queryset to JSON format
    booking_data = []
    for booking in bookings:
        
        booking_data.append({
            'room_name': booking.room.room_name,
            'username': booking.user.username,
            'payment_status': booking.payment_status,
            'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'),  # Convert date to string
            'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'),  # Convert date to string
        })


    if room.max_room > len(booking_data):
      
        checkindate= request.GET.get("check_in_date")
        checkin_date = timezone.datetime.strptime(checkindate, '%Y-%m-%d').date()
        checkoutdate=request.GET.get("check_out_date")
        checkout_date = timezone.datetime.strptime(checkoutdate, '%Y-%m-%d').date()
        # Check if the latest checkout date is earlier than the check-in date
        return JsonResponse({'bookings': booking_data,"status":0})
    else:
        return JsonResponse({'message': latest_booking.check_out_date,"status":1})
     
    # Return JSON response
    return JsonResponse({'bookings': booking_data,"status":0})

def send_extend_error(request):
    booking_id = request.GET.get('booking_id')
    

    
    
    booking = Booking.objects.get(pk=booking_id)
    send_extension_error(booking.user.email)






def booking_list_filter(request):

    checkin_date= request.GET.get("check_in_date")
    checkout_date=request.GET.get("check_out_date")

    adult=int(request.GET.get("adult"))
    child=int(request.GET.get('child'))

    checkin_date = timezone.datetime.strptime(checkin_date, '%Y-%m-%d').date()
    checkout_date = timezone.datetime.strptime(checkout_date, '%Y-%m-%d').date()
    print(adult,child)
    if checkout_date < checkin_date:
        return JsonResponse({'message': 'Checkout date should be after the Checkin date',"status":2})
    
    bookings = Booking.objects.filter(
        Q(check_in_date__lt=checkout_date, check_out_date__gt=checkin_date) |
        Q(check_in_date__gte=checkin_date, check_out_date__lte=checkout_date) |
        Q(check_in_date__lt=checkin_date, check_out_date__gt=checkout_date)
    )
    
    room_list=Room.objects.filter(
        Q(number_of_adult__gte=adult) & Q(number_of_children__gte=child)
    )
    for room in room_list:
        print(room.room_name)
    
    latest_booking=0
    if bookings:
        bookings = bookings.order_by('-check_out_date')
        # Get the latest booking (first booking in the ordered queryset)
        latest_booking = bookings.first()
    
    # Convert queryset to JSON format
    booking_data = []
    for booking in bookings: 
        booking_data.append({
            'room_name': booking.room.room_name,
            'username': booking.user.username,
            'payment_status': booking.payment_status,
            'check_in_date': booking.check_in_date.strftime('%Y-%m-%d'),  # Convert date to string
            'check_out_date': booking.check_out_date.strftime('%Y-%m-%d'),  # Convert date to string
        })


    status=1
    room_counts = {}  # Dictionary to store counts for each room

    for booking_info in booking_data:
        room_name = booking_info['room_name']
        room_counts[room_name] = room_counts.get(room_name, 0) + 1

    available_rooms={}
        
    for room in room_list:
        room_name=room.room_name
        booking_count = room_counts.get(room_name, 0)
        if room.max_room > booking_count:
            available_rooms[room.room_name]=room.max_room-booking_count
            status=0
            checkindate= request.GET.get("check_in_date")
            checkin_date = timezone.datetime.strptime(checkindate, '%Y-%m-%d').date()
            checkoutdate=request.GET.get("check_out_date")
            checkout_date = timezone.datetime.strptime(checkoutdate, '%Y-%m-%d').date()

    if status==0:
        return JsonResponse({'bookings': available_rooms,"status":0})

    return JsonResponse({'message': latest_booking.check_out_date,"status":1})




@user_required
def BookAvailableRoom(request):
    # Retrieve the room object using the ID
    room_id=request.GET.get("id")
    room = Room.objects.get(id=room_id)
    

    # Retrieve room ID from the POST request
   
    checkin_str = request.GET.get('check_in_date')  # Assuming 'checkin' is a string in format YYYY-MM-DD
    checkout_str = request.GET.get('check_out_date')  # Assuming 'checkout' is a string in format YYYY-MM-DD


    # Convert string dates to Python date objects
    checkin_date = datetime.strptime(checkin_str, '%Y-%m-%d').date()
    checkout_date = datetime.strptime(checkout_str, '%Y-%m-%d').date()


        # Save the booking data to the Booking model
    booking = Booking.objects.create(
            user=request.user,
            room_id=int(room_id),
            check_in_date=checkin_date,
            check_out_date=checkout_date,
            payment_status="Pending",
        )

    room.save()
        
        # Return a JSON response indicating success
    return JsonResponse({'message': 'Booking successful'})
        
       
    
    # Return an error response if the request method is not POST
    return render(request, 'dashboard/book-room.html', {'room': room})

def UserFeedback(request):
    return render(request, 'dashboard/user-feedback.html')

def Feedbacks(request):
    
    all_feedback = Feedback.objects.all()

    # Pass the data to the template for rendering
    return render(request, 'dashboard/feedbacks.html', {'all_feedback': all_feedback})



@csrf_exempt
def store_feedback_api(request):
    if request.method == 'POST':
        # Get the feedback data from the request
        data = json.loads(request.body.decode('utf-8'))
        feedback_text = data.get('feedback')

        # Create a new Feedback object and save it to the database
        feedback = Feedback.objects.create(user=request.user,feedback=feedback_text)

        # Return a success response
        return JsonResponse({'message': 'Feedback stored successfully'}, status=201)

    # If the request method is not POST, return a 405 Method Not Allowed response
    return JsonResponse({'error': 'Method Not Allowed'}, status=405)

from datetime import date

def Extend(request, id):
    # Filter bookings based on the user and checkout date
    bookings = Booking.objects.filter(user__id=id, check_out_date__gte=date.today())

    # Create the context dictionary
    context = {
        'bookings': bookings,
    }

    # Render the extend.html template with the context
    return render(request, 'dashboard/extend.html', context=context)

def ExtendForm(request):
    id=request.GET.get('id')
    room=request.GET.get('room')
    booking = get_object_or_404(Booking, id=id)
    
    # Pass the booking object to the template context
    context = {
        'booking': booking,
    }

    return render(request,'dashboard/extendform.html',context=context)


@require_GET
def update_checkout_date(request):
    # Get the booking ID and new checkout date from the URL parameters
    booking_id = request.GET.get('booking_id')
    new_checkout_date = request.GET.get('checkout_date')

    
        # Retrieve the booking object based on the booking ID
    booking = Booking.objects.get(pk=booking_id)
        # Update the checkout date
    booking.check_out_date = new_checkout_date
    booking.payment_status = "Partial"

    send_extension(booking.user.email, new_checkout_date)

    print('hi')
    # Save the changes
    booking.save()
    return JsonResponse({'message': 'Checkout date updated successfully'})




def generate_signature(total_amount, transaction_uuid, product_code, secret):
    # Concatenate the necessary fields
    data = f"total_amount={total_amount},transaction_uuid={transaction_uuid},product_code={product_code}"
    
    # Calculate HMAC SHA256
    hashed = hmac.new(secret.encode(), data.encode(), hashlib.sha256)
    
    # Encode to base64
    signature = base64.b64encode(hashed.digest()).decode()
    
    return signature

import uuid

@csrf_exempt
def payment_view(request):
    if request.method == 'POST':
        # Extract form data
        total_amount = request.POST.get('total_amount')
        transaction_uuid = str(uuid.uuid4())
        product_code = request.POST.get('product_code')
        secret = request.POST.get('secret')
        print(transaction_uuid)
       
        # Generate signature
        signature = generate_signature(total_amount, transaction_uuid, product_code, secret)

        # Redirect to the eSewa URL with form data and signature
        redirect_url = 'https://rc-epay.esewa.com.np/api/epay/main/v2/form'
        form_data = {
            'amount': total_amount,
            'tax_amount': '0',
            'total_amount': total_amount,
            'transaction_uuid': transaction_uuid,
            'product_code': product_code,
            'product_service_charge': '0',
            'product_delivery_charge': '0',
            'success_url': 'http://localhost:8000/payment-success/',
            'failure_url': 'https://developer.esewa.com.np/failure',
            'signed_field_names': 'total_amount,transaction_uuid,product_code',
            'signature': signature,
            'secret': secret
        }
        # if request.user.is_authenticated:
            # Creating dummy payment data for the current user
            # payment = Payment.objects.create(
            #     user=request.user,
            #     service='esewa',
            #     payment_date=timezone.now(),
            #     amount=total_amount, 
            #     transaction_uuid=transaction_uuid, 
            #     status=False
            # )
            # payment.save()
        return render(request, 'dashboard/redirect_to_esewa.html', {'redirect_url': redirect_url, 'form_data': form_data})
    return render(request,'dashboard/esewa.html')
    


def esewa(request):
    # try:
    #     payment=Payment.objects.get(user=request.user,status=True)
    #     return render(request,'dashboard/pro_user.html')
    # except Exception as e:
        return render(request,'dashboard/pay.html')


def payment_success(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        checkin_date = data.get('checkin')
        checkout_date = data.get('checkout')
        roomId = data.get('roomId')
        # Convert string dates to datetime objects
        
        checkin_date = datetime.strptime(checkin_date, '%Y-%m-%d').date()
        checkout_date = datetime.strptime(checkout_date, '%Y-%m-%d').date()
        
           

        # Filter bookings based on check-in and check-out dates
        bookings = Booking.objects.filter(check_in_date=checkin_date, check_out_date=checkout_date,user=request.user,room__id=roomId).first()
        print(checkin_date,checkout_date,request.user.username,roomId)
        bookings.payment_status="Paid"
      
        bookings.save()
        return render(request, 'dashboard/payment_success.html')
    if request.method == 'GET':
        encoded_string = request.GET.get('data')
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_string = decoded_bytes.decode('utf-8')
        transaction_data = json.loads(decoded_string)
        print(transaction_data)

        transaction_uuid = transaction_data['transaction_uuid']
        amount = transaction_data['total_amount']
        print("amount",amount)
        send_confirmation_email(request.user.email,amount)
     
        
          
        return render(request, 'dashboard/payment_success.html')
       
from django.core.serializers import serialize
def total_staff_dash(request):
    total_users = CustomUser.objects.filter(is_staff=False, is_superuser=False).count()
    all_users = CustomUser.objects.filter(is_staff=False, is_superuser=False)
    total_pending = Booking.objects.filter(payment_status='Pending').count()
    total_feedback = Feedback.objects.count()

    # Serialize the QuerySet to JSON
    all_users_serialized = json.loads(serialize('json', all_users))

    data = {
        'total_users': total_users,
        'total_pending': total_pending,
        'total_feedback': total_feedback,
        'all_users': all_users_serialized
    }

    return JsonResponse(data)






def toggle_review_display(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(Review, id=review_id)
        review.display_on_website = not review.display_on_website
        review.save()
        return JsonResponse({'success': True, 'display_on_website': review.display_on_website})
    return JsonResponse({'success': False})

   


@require_GET
def total_price_by_checkout_date(request):
    data = Booking.objects.values('check_out_date').annotate(total_price=Sum('price')).order_by('check_out_date')
    return JsonResponse(list(data), safe=False)
