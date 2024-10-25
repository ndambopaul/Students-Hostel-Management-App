from django.urls import path
from apps.hostels.views import hostel_bookings, book_hostel, bookings_home

urlpatterns = [
    path("bookings/", hostel_bookings, name="bookings"),
    path("hostel-booking/", bookings_home, name="hostel-booking"),
    path("book-hostel/", book_hostel, name="book-hostel"),
]