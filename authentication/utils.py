
from django.conf import settings
from django.core.mail import send_mail

def send_email_token(email,token):

    try:

            subject = 'Account verification'
            message = f'Welcome to The Urban Escape Hotel !\nPlease click on the link  to verify your account and proceed with the login : http://127.0.0.1:8000/verify/{token}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            send_mail( subject, message, email_from, recipient_list )


    except Exception as e:
            return False

    return True

def send_password_token(email, token):
    try:
        subject = 'Password Reset'
        message = f'You requested a password reset for your account.\nPlease click on the link to reset your password: http://127.0.0.1:8000/reset-password/{token}/'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail(subject, message, email_from, recipient_list)
    except Exception as e:
        return False
    return True