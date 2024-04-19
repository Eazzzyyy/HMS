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
