from django.urls import path

from . import views


urlpatterns = [
    path('login/',views.Login, name='login'), # domain.com/login/
    path('register/',views.Register, name='register'), 
    # path('dashboard/',views.Dashboard, name='dashboard'), 
    path('verify/<str:token>/',views.VerifyEmail,name='verify_email'),
    path('forgot-password/',views.ForgotPassword,name='forgot_password'),
    path('reset-password/<str:token>/',views.ResetPassword,name='reset_password'),# the third parameter can be used when using the '{% url %}' template tag to refer to a urlpattern
    path('auth-receiver', views.auth_receiver, name='auth_receiver'),
    path('askContact/', views.askContact, name='askContact'),
    path('content/', views.content, name='content'),


]
