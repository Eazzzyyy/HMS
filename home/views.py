from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Create your views here.
def Homepage(request):
   rooms = Room.objects.all()
   return render(request,'home/homepage.html',{'rooms':rooms })