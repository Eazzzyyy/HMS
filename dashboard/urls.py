from django.urls import path

from . import views


urlpatterns = [ 
    
    # path('staff-dashboard/',views.StaffDashboard, name='staff_dashboard'), 
    path('bookings/', views.UserBookings, name='user_bookings'),
    path('payment/', views.Payment, name='payment'),
    path('reviews-ratings', views.ReviewRating, name='reviews_rating'),
    path('profile/', views.Profile, name='profile'),
    path('admin-dashboard/', views.AdminDashboard, name='admin-dashboard'),
    path('staffs/', views.Staffs, name='staffs'),
    path('create-staff/', views.CreateStaff, name='create-staff'),
    path('rooms/', views.Rooms, name='rooms'),
    path('create-room/', views.CreateRoom, name='create-room'),
    path('edit-staff/<id>', views.EditStaff, name='edit-staff'),
    path('delete-staff/<id>/', views.delete_user, name='delete-staff'),
    # path('delete-staff/', views.DeleteStaff, name='delete-staff'),
]
