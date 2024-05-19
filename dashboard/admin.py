from django.contrib import admin

from .models import Booking,Feedback, Review

class BookingAdmin(admin.ModelAdmin):
   
    list_display = ('id', 'room', 'user', 'user_first_name', 'user_last_name', 'payment_status', 'check_in_date', 'check_out_date')

  
    def user_first_name(self, obj):
        return obj.user.first_name

    
    def user_last_name(self, obj):
        return obj.user.last_name

    
    user_first_name.short_description = 'First Name'
    user_last_name.short_description = 'Last Name'

admin.site.register(Booking, BookingAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback', 'date')
  
admin.site.register(Feedback, FeedbackAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'review_message','rating'
    )
admin.site.register(Review, ReviewAdmin)