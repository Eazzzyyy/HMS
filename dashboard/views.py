from django.shortcuts import redirect, render
from authentication.models import CustomUser
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse

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


