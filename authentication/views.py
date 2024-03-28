import uuid
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .utils import *
import re
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests







def Login(request):
    context={ 'username':''

    }
    if request.method == 'POST':
        username=request.POST['username']
        pass1=request.POST['pass1']

        context={ 'username':username

            }
     


        user= authenticate(username=username, password=pass1)
        if user is not None and user.is_verified:  # Check if user is verified
            login(request, user)
            fname = user.first_name
            return render(request, 'dashboard/user-bookings.html', {'fname': fname})
          
        elif user is not None and not user.is_verified:
            messages.error(request, "Your email is not verified yet. Please check your email for verification.")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'authentication/login.html',context)



import re

def Register(request):
    context = {
        'username': '',
        'fname': '',
        'lname': '',
        'email': '',
        'contact': '',
        'pass1': '',
        'pass2': '',
        'errors': {}  # Initialize empty dictionary for error messages
    }

    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        contact = request.POST['contact']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        context = {
            'username': username,
            'fname': fname,
            'lname': lname,
            'email': email,
            'contact': contact,
            'pass1': pass1,
            'pass2': pass2,
            'errors': {}  # Reset errors dictionary for each request
        }

        status = False

        if CustomUser.objects.filter(username=username).exists():
            context['errors']['username'] = "Username is already in use. Please choose a different username."
            status = True
      
        if CustomUser.objects.filter(email=email).exists():
            context['errors']['email'] = "Email address is already in use. Please use a different email."
            status = True

        if len(username) > 15:
            context['errors']['username'] = "The username cannot be longer than 15 characters."
            status = True

        if pass1 != pass2:
            context['errors']['pass1'] = "The passwords don't match."
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
            return render(request, 'authentication/register.html', context)

        email_token = str(uuid.uuid4())
        my_user = CustomUser.objects.create_user(username, email, pass1)
        my_user.first_name = fname
        my_user.last_name = lname
        my_user.contact_number = contact
        my_user.email_token = email_token
        my_user.save()

        send_email_token(email, email_token)
        messages.success(request, "Your account was successfully created. Please check your email for verification.")
        return redirect('login')

    return render(request, 'authentication/register.html', context)


def VerifyEmail(request, token):
    try:
        user = CustomUser.objects.get(email_token=token)
        user.is_verified = True
        user.save()
        messages.success(request, "Your email has been verified. You can now log in.")
    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid verification token.")

    return redirect('login')



def ForgotPassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')

        try:
            user = CustomUser.objects.get(username=username)
            email= user.email

            # Generate a unique token for password reset
            password_token = str(uuid.uuid4())
            user.password_reset_token = password_token
            user.save()
            send_password_token(email,password_token)

        
            messages.success(request, "Password reset link has been sent to your email.")
            print(request.POST.get('hiddencheck'))
            if request.POST.get('hiddencheck'):
                return redirect(f'/forgot-password?type=change&username={request.user.username}')
            return redirect('forgot_password')

        except CustomUser.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')
    return render(request, 'authentication/forgot-password.html')



def ResetPassword(request, token):
   
    try:
        user = CustomUser.objects.get(password_reset_token=token)
        
        if request.method == 'POST':
            new_password = request.POST.get('new-password')
            confirm_password = request.POST.get('confirm-password')
           

            if new_password != confirm_password:
                messages.error(request, "Passwords don't match")
                return redirect(f'/reset-password/{token}/')
            
            alphanumeric_pattern = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$')

            if not alphanumeric_pattern.match(new_password):
                messages.error(request, "The password must be alphanumeric and contain atleast 8 characters.")
                return redirect(f'/reset-password/{token}/')
            
         
            user.set_password(new_password)
            user.save()
            messages.success(request,"Your password was reset successfully!")
            return redirect('login')

    except CustomUser.DoesNotExist:
        messages.error(request, "Invalid password reset token")
        return redirect('forgot_password')

    return render(request, 'authentication/reset-password.html')




@csrf_exempt
def auth_receiver(request):
    """
    Google calls this URL after the user has signed in with their Google account.
    """
    token = request.POST['credential']

    try:
        user_data = id_token.verify_oauth2_token(
            token, requests.Request(), '138438340790-6opvfcoffef79m80lr2g0lic3btjvq92.apps.googleusercontent.com'
        )
        print(user_data)
        
    except ValueError:
    
        return HttpResponse(status=403)

    try:
        user = CustomUser.objects.get(email=user_data['email'])
        # Log in the user
        login(request, user)

        # Redirect to dashboard if user exists
        return redirect('user_bookings')
    except CustomUser.DoesNotExist:
        
        user = CustomUser.objects.create_user(
            username=user_data['email'],  
            email=user_data['email'],
            first_name=user_data.get('given_name', ''),
            last_name=user_data.get('family_name', ''),
            is_verified=True
        )

    # Log in the user
    login(request, user)

    return redirect('askContact')


def askContact(request):
    if request.method == 'POST':
        contact = request.POST.get('contact_number')
        status=False
        if CustomUser.objects.filter(contact_number=contact):    
          status=True
          messages.error(request, "The contact number is already in use. Please choose a different contact number.")
        
        if len(str(contact)) !=10:
            status=True
     
            messages.error(request, "The contact number should be exactly 10 digits" )

            # send eror message here and dont let other code below it run
        if status:
            # If there are errors, render the form again with error messages
            return render(request, 'authentication/ask_contact.html')

        request.user.contact_number = contact
        request.user.save()
        return redirect('user_dashboard')  
    
    return render(request, 'authentication/ask_contact.html')











