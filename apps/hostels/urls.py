from django.urls import path
from apps.hostels.views import (
    hostels,
    new_hostel,
    hostel_bookings,
    edit_booking,
    book_hostel,
    bookings_home,
    booking_details,
    hostel_rooms,
    new_hostel_room
)

urlpatterns = [
    path("", hostels, name="hostels"),
    path("new-hostel/", new_hostel, name="new-hostel"),
    path("bookings/", hostel_bookings, name="bookings"),
    path("bookings/<int:id>/details", booking_details, name="booking-details"),
    path("edit-booking/", edit_booking, name="edit-booking"),
    path("hostel-booking/", bookings_home, name="hostel-booking"),
    path("book-hostel/", book_hostel, name="book-hostel"),
    path("hostel-rooms/", hostel_rooms, name="hostel-rooms"),
    path("new-hostel-room/", new_hostel_room, name="new-hostel-room"),
]
