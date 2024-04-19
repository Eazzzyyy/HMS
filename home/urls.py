from django.urls import path

from . import views

from authentication.views import Login



urlpatterns = [
    path('',views.Homepage,name='home') ,# domain.com/login
    path('api/check-login/', views.check_login_status, name='check_login_status'),
    path('logout/',views.logout_view,name='logout')

]



