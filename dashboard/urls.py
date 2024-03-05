from django.urls import path

from . import views


urlpatterns = [ 
    
    # path('staff-dashboard/',views.StaffDashboard, name='staff_dashboard'), 
    path('bookings/', views.UserBookings, name='user_bookings'),
    path('payment/', views.Payment, name='payment'),
    path('reviews-ratings', views.ReviewRating, name='reviews_rating'),
    path('profile', views.Profile, name='profile'),

]
