import re
from django.shortcuts import redirect, render
from authentication.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
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
    if request.method == 'POST':
        # Extract JSON data from request body
        data = json.loads(request.body)
        
        # Extract firstname, lastname, and contact number from JSON data
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        contact_number = data.get('contact_number')

        # Get the current user object
        user = CustomUser.objects.get(username=request.user.username)
        
        # Validation
        errors = {}

        if len(str(contact_number)) != 10:
            errors['contact'] = "The contact number should be exactly 10 digits."

        if CustomUser.objects.exclude(username=user.username).filter(contact_number=contact_number).exists():
            errors['contact'] = "The contact number is already in use. Please choose a different contact number."
        
        if 'contact' in errors:
        
            # If there are errors, render the profile page with errors displayed
            return JsonResponse(errors)
        else:
            print("valid")
            # Update user information
            user.first_name = first_name
            user.last_name = last_name
            user.contact_number = contact_number
            # Save the updated user object
            user.save()
          
            errors['success']="Saved successfully!"
            return JsonResponse(errors)

    # If request method is not POST or there are no errors, render the profile page
    return render(request, 'dashboard/profile.html', {'username': request.user.username, 'errors': {}})


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
        return render(request, 'dashboard/create-staff.html',context)

    return render(request, 'dashboard/create-staff.html')

def Rooms(request):
    return render(request, 'dashboard/rooms.html')

def CreateRoom(request):
    return render(request, 'dashboard/create-room.html')

def EditStaff(request, id):
    
    if request.method == "POST":
        staff_member = CustomUser.objects.get(id=id)
        print(id)
        staff_member.first_name = request.POST.get('fname')
        staff_member.last_name = request.POST.get('lname')
        staff_member.username = request.POST.get('username')
        staff_member.contact_number = request.POST.get('contact')
        staff_member.save()
        staff_member = CustomUser.objects.get(id=id)
        context = {'staff_member': staff_member}
        # Redirect to a success page or another page after updating the staff member

        return render(request, 'dashboard/edit-staff.html', context)  # Replace 'success_page' with the name of your success page URL
    else:
        staff_member = CustomUser.objects.get(id=id)
        context = {'staff_member': staff_member}
        return render(request, 'dashboard/edit-staff.html', context)
    
    
@csrf_exempt  # You may want to handle CSRF protection differently based on your application requirements
def delete_user(request, id):
    print("lol")
    try:
        user = CustomUser.objects.get(id=id)
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'}, status=200)
    except CustomUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
