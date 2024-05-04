from django.urls import path

from . import views
from .views import store_feedback_api
from .views import update_checkout_date

urlpatterns = [ 
    
    path('staff-dashboard/',views.StaffDashboard, name='staff_dashboard'), 
    path('bookings/', views.UserBookings, name='user_bookings'),
    path('payment/', views.Payment, name='payment'),
    path('reviews-ratings', views.ReviewRating, name='reviews_rating'),
    path('profile/', views.Profile, name='profile'),
    path('admin-dashboard/', views.AdminDashboard, name='admin-dashboard'),
    path('staffs/', views.Staffs, name='staffs'),
    path('create-staff/', views.CreateStaff, name='create-staff'),
    path('edit-staff/<id>/', views.EditStaff, name='edit-staff'),
    path('delete-staff/<id>/', views.DeleteStaff, name='delete-staff'),
    path('rooms/', views.Rooms, name='rooms'),
    path('create-room/', views.CreateRoom, name='create-room'),
    path('edit-room/<id>', views.EditRoom, name='edit-room'),
    path('admin-reviews-ratings/', views.admin_reviews_ratings, name='admin-reviews-ratings'),
    path('delete-room/<id>/', views.DeleteRoom, name='delete-room'),
    path('book/<id>/', views.BookRoom, name='book-room'),
    path('bookingstatus/<roomname>/', views.booking_list, name='booking-list'),
    path('staff-profile/', views.StaffProfile, name='staff-profile'),
    path('booking_list_filter/',views.booking_list_filter,name='filter_booking'),
    path('book-available-room/',views.BookAvailableRoom, name='book-available-room'),
    path('staff-book-room/', views.StaffBookRoom, name='staff-book-room'),
    path('user-feedback/', views.UserFeedback, name='user-feedback'),
    path('feedbacks/', views.Feedbacks, name='feedbacks'),
    path('api/store-feedback/', store_feedback_api, name='store_feedback_api'),
    path('view-extend/<id>/', views.Extend, name='extend'),
    path('extend/',views.ExtendForm,name='extend_booking'),
    path('update-checkout-date/', update_checkout_date, name='update_checkout_date'),
]
