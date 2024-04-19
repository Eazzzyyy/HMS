from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from .models import Room
from django.contrib.auth import logout
from django.shortcuts import redirect



def Homepage(request):
   rooms = Room.objects.all()
   return render(request,'home/homepage.html',{'rooms':rooms })


def check_login_status(request):
    if request.user.is_authenticated:
        return JsonResponse({'logged_in': True,'user':request.user.username})
    else:
        return JsonResponse({'logged_in': False})
    


def logout_view(request):
    logout(request)
    return redirect('home')
