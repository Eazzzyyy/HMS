from django.urls import path

from . import views

from authentication.views import Login



urlpatterns = [
    path('',views.Homepage,name='home') ,# domain.com/login
    path('api/check-login/', views.check_login_status, name='check_login_status'),
    path('logout/',views.logout_view,name='logout'),
    path('available-rooms/',views.room_available),
     path('total-max-rooms/', views.total_max_rooms, name='total_max_rooms'),
    path('api/room/<int:room_id>/price/', views.get_room_price, name='get_room_price'),


]



