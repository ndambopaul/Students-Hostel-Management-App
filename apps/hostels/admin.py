from django.contrib import admin

from apps.hostels.models import Booking
# Register your models here.
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone_number", "status", "created_on")
