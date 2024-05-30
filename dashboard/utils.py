from django.contrib.auth.decorators import user_passes_test
from functools import wraps

from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from django.urls import reverse_lazy


def admin_required(view_func):
    """
    Decorator for views that checks whether the user is an admin.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You do not have permission to access this page")
            pass  # Replace this with your desired action
    return _wrapped_view


def user_required(view_func):
  """
  Decorator for views that checks whether the user is logged in.
  If the user is logged in, the view is executed normally.
  If not, the user is redirected to a login page.
  """
  @wraps(view_func)
  def _wrapped_view(request, *args, **kwargs):
    if request.user.is_authenticated:
      print("User is authenticated!")  # For debugging purposes
      return view_func(request, *args, **kwargs)
    else:
      return redirect(reverse_lazy('login'))  # Redirect to login
  return _wrapped_view


def staff_required(view_func):
    """
    Decorator for views that checks whether the user is a staff member.
    If the user is a staff member, the view is executed normally.
    If not, the user is redirected to a login page.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            print("User is a staff member!")  # For debugging purposes
            return view_func(request, *args, **kwargs)
        else:
            return redirect(reverse_lazy('uelogin'))  # Redirect to login
    return _wrapped_view



from django.conf import settings
from django.core.mail import send_mail



def send_booking_email(email):

    try:

            subject = 'Room has been booked'
            message = f'Please click on the link to check your status : http://127.0.0.1:8000/bookings.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )


    except Exception as e:
            return False

    return True


def send_confirmation_email(email,price):

    try:

            subject = 'Payment Successful'
            message = f'Your payment  has been received. Please provide your review '
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )


    except Exception as e:
            return False

    return True



def send_extension(email,new_date):

    try:

            subject = 'Booking extended'
            message = f'Your booking is extended to {new_date}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )


    except Exception as e:
            return False

    return True


def send_extension_error(email):

    try:

            subject = 'Booking extension failure'
            message = f'Sorry, the booking cannot be exented because it is already allocated'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )


    except Exception as e:
            return False

    return True