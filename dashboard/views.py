from django.shortcuts import render

# Create your views here.


def UserBookings(request):
     return render(request, 'dashboard/user-bookings.html')

def Payment(request):
     return render(request, 'dashboard/payment.html')

def ReviewRating(request):
         return render(request, 'dashboard/reviews-rating.html')

def Profile(request):
         return render(request, 'dashboard/profile.html')