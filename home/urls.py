from django.urls import path

from . import views



urlpatterns = [
    path('',views.Homepage) # domain.com/login
]