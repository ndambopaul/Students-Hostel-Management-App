from django.db import models

from apps.core.models import AbsoluteBaseModel

# Create your models here.
BOOKING_STATUSES = (
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
    ("Confirmed", "Confirmed"),
)

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)

class Hostel(AbsoluteBaseModel):
    name = models.CharField(max_length=255)
    rooms = models.IntegerField(default=1)
    capacity = models.IntegerField(default=1)

    def __str__(self):
        
        return self.name


class HostelRoom(AbsoluteBaseModel):
    hostel = models.ForeignKey("hostels.Hostel", on_delete=models.CASCADE, null=True)
    room_number = models.CharField(max_length=255)
    room_capacity = models.IntegerField(default=1)
    students_assigned = models.IntegerField(default=0)
    fully_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.room_number

    def status(self):
        return "Fully Booked" if self.fully_booked else "Available"


class Booking(AbsoluteBaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    gender = models.CharField(max_length=255, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=255)
    guardian_name = models.CharField(max_length=255)
    guardian_phone_number = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=255)
    mpesa_code = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=BOOKING_STATUSES, default="Pending")
    room_assigned = models.ForeignKey("hostels.HostelRoom", on_delete=models.CASCADE, null=True)
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
