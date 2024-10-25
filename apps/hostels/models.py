from django.db import models

from apps.core.models import AbsoluteBaseModel
# Create your models here.
BOOKING_STATUSES = (
    ("Pending", "Pending"),
    ("Approved", "Approved"),
    ("Rejected", "Rejected"),
)

GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),
)
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
    

    def __str__(self):
        return f"{self.first_name} {self.last_name}"