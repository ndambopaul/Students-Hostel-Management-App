from datetime import datetime, timedelta
import calendar

from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from django.db import transaction

from apps.hostels.models import Booking
number_of_rooms = 4
# Create your views here.
def hostel_bookings(request):
    bookings = Booking.objects.annotate(
        is_pending=Case(
            When(status='Pending', then=Value(0)),  # Pending bookings are given a value of 0
            default=Value(1),  # All other statuses are given a value of 1
            output_field=IntegerField(),
        )
    ).order_by("-created_on")
    
    if request.method == "POST":
        search = request.POST.get("search")
        if search:
            bookings = bookings.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(registration_number__icontains=search)
            )
    
    paginator = Paginator(bookings, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj
    }
    return render(request, "hostels/bookings/bookings.html", context)


def bookings_home(request):
    booking = None
    total_bookings = Booking.objects.count()
    if request.method == "POST":
        search = request.POST.get("search_text")
        if search:
            booking = Booking.objects.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search) |
                Q(registration_number__icontains=search)
            ).first()
            
            if booking:
                something_found = True
                print(f"Booking ID: {booking.id}, Student: {booking.first_name} {booking.last_name}")
    
    context = {
        "can_book": True if total_bookings < number_of_rooms else False,
        "booking": booking
    }
    
    print(context)
    
    return render(request, "hostels/bookings/bookings_home.html", context)

def book_hostel(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        registration_number = request.POST.get("registration_number")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        amount = request.POST.get("amount")
        mpesa_code = request.POST.get("mpesa_code")
        
        guardian_name = request.POST.get("guardian_name")
        guardian_phone_number = request.POST.get("guardian_phone_number")
        
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        
        booking = Booking.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            registration_number=registration_number,
            gender=gender,
            phone_number=phone_number,
            guardian_name=guardian_name,
            guardian_phone_number=guardian_phone_number,
            address=address,
            city=city,
            country=country,
            status="Pending",
            amount=amount,
            mpesa_code=mpesa_code,
        )
        
        return redirect("hostel-booking")
        
        messages.success(request, "Hostel booking successful.")
    return render(request, "hostels/bookings/book_hostel.html")