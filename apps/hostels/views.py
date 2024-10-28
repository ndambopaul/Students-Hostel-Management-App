from datetime import datetime, timedelta
import calendar

from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Case, When, Value, IntegerField
from django.db import transaction

from apps.hostels.models import Booking, HostelRoom, Hostel
from apps.students.models import Student
from apps.payments.models import RentPayment
from apps.users.models import User
from apps.core.models import UserRole

number_of_rooms = 4

BOOKING_STATUSES = ["Pending", "Approved", "Rejected"]


# Create your views here.
def hostels(request):
    hostels = Hostel.objects.all()
    context = {
        "hostels": hostels,
    }
    return render(request, "hostels/hostels.html", context)


def new_hostel(request):
    if request.method == "POST":
        name = request.POST.get("name")
        rooms = request.POST.get("rooms")
        capacity = request.POST.get("capacity")

        Hostel.objects.create(name=name, rooms=rooms, capacity=capacity)
        return redirect("hostels")
    return render(request, "hostels/new_hostel.html")


def hostel_details(request, id):
    hostel = Hostel.objects.get(id=id)
    
    hostel_students = Student.objects.filter(room_assigned__hostel_id=id)
    
    students = Student.objects.all()
    
    paginator = Paginator(hostel_students, 6)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "hostel": hostel,
        "page_obj": page_obj,
        "students": students,
    }
    return render(request, "hostels/hostel_details.html", context)

def edit_hostel(request):
    if request.method == "POST":
        id = request.POST.get("hostel_id")
        name = request.POST.get("name")
        rooms = request.POST.get("rooms")
        capacity = request.POST.get("capacity")

        hostel = Hostel.objects.get(id=id)
        hostel.name = name
        hostel.rooms = rooms
        hostel.capacity = capacity
        hostel.save()
        return redirect("hostels")
    return render(request, "hostels/edit_hostel.html")


def delete_hostel(request):
    if request.method == "POST":
        id = request.POST.get("hostel_id")
        Hostel.objects.get(id=id).delete()
        return redirect("hostels")
    return render(request, "hostels/delete_hostel.html")


def hostel_bookings(request):
    bookings = Booking.objects.annotate(
        is_pending=Case(
            When(
                status="Pending", then=Value(0)
            ),  # Pending bookings are given a value of 0
            default=Value(1),  # All other statuses are given a value of 1
            output_field=IntegerField(),
        )
    ).order_by("-created_on")

    if request.method == "POST":
        search = request.POST.get("search")
        if search:
            bookings = bookings.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
                | Q(registration_number__icontains=search)
            )

    paginator = Paginator(bookings, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    rooms = HostelRoom.objects.all()

    context = {
        "page_obj": page_obj, 
        "booking_statuses": BOOKING_STATUSES,
        "rooms": rooms
    }
    return render(request, "hostels/bookings/bookings.html", context)


def booking_details(request, id):
    booking = Booking.objects.get(id=id)
    
    rooms = HostelRoom.objects.all()
    
    context = {"booking": booking, "rooms": rooms}
    return render(request, "hostels/bookings/booking_details.html", context)


def edit_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        status = request.POST.get("status")

        booking = Booking.objects.get(id=booking_id)
        booking.status = status
        booking.save()

        return redirect("bookings")

    return render(request, "hostels/bookings/edit_booking.html")


def bookings_home(request):
    booking = None
    total_bookings = Booking.objects.count()
    if request.method == "POST":
        search = request.POST.get("search_text")
        if search:
            booking = Booking.objects.filter(
                Q(first_name__icontains=search)
                | Q(last_name__icontains=search)
                | Q(email__icontains=search)
                | Q(registration_number__icontains=search)
            ).first()

            if booking:
                something_found = True
                print(
                    f"Booking ID: {booking.id}, Student: {booking.first_name} {booking.last_name}"
                )

    context = {
        "can_book": True if total_bookings < number_of_rooms else False,
        "booking": booking,
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


@transaction.atomic
def approve_booking(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        room_id = request.POST.get("room_id")
        
        booking = Booking.objects.get(id=booking_id)
        room = HostelRoom.objects.get(id=room_id)
        
        user = User.objects.create(
            first_name=booking.first_name,
            last_name=booking.last_name,
            email=booking.email,
            username=booking.email,
            role=UserRole.objects.get(name="Student"),
            phone_number=booking.phone_number,
            address=booking.address,
            city=booking.city,
            country=booking.country,
            gender=booking.gender,
        )
        
        user.set_password("1234")
        user.save()

        student = Student.objects.create(
            user=user,
            registration_number=booking.registration_number,
            room_assigned=room,
            hostel_assigned=room.hostel,
            guardian_name=booking.guardian_name,
            guardian_phone_number=booking.guardian_phone_number,
            status="Pending Check-In"
        )
        
        room.students_assigned += 1
        room.save()
        
        booking.status = "Approved"
        booking.save()
        
        RentPayment.objects.create(
            student=student,
            amount=booking.amount,
            transaction_code=booking.mpesa_code,
            payment_date=booking.created_on.date()
        )
        
        return redirect("bookings")
        

    return render(request, "hostels/bookings/approve_booking.html")


def hostel_rooms(request):
    hostel_rooms = HostelRoom.objects.all()
    hostels = Hostel.objects.all()
    
    if request.method == "POST":
        search_text = request.POST.get("search_text")
        if search_text:
            hostel_rooms = HostelRoom.objects.filter(
                Q(room_number__icontains=search_text)
            )
    
    paginator = Paginator(hostel_rooms, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    context = {
        "page_obj": page_obj,
        "hostels": hostels
    }
    
    return render(request, "hostels/rooms/rooms.html", context)

def hostel_room_details(request, id):
    room = HostelRoom.objects.get(id=id)
    room_students = Student.objects.filter(room_assigned_id=id)
    
    students = Student.objects.filter(room_assigned=None)
    
    context = {
        "room": room,
        "room_students": room_students,
        "students": students,
    }
    
    return render(request, "hostels/rooms/room_details.html", context)

def new_hostel_room(request):
    if request.method == "POST":
        hostel = request.POST.get("hostel")
        room_number = request.POST.get("room_number")
        room_capacity = request.POST.get("room_capacity")

        HostelRoom.objects.create(hostel_id=hostel, room_number=room_number, room_capacity=room_capacity)
        
        return redirect("hostel-rooms")
    return render(request, "hostels/rooms/new_room.html")


def delete_hostel_room(request):
    if request.method == "POST":
        room_id = request.POST.get("room_id")
        room = HostelRoom.objects.get(id=room_id)
        room.delete()
        return redirect("hostel-rooms")
    return render(request, "hostels/rooms/delete_room.html")


def add_student_to_room(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        room_id = request.POST.get("room_id")
            
        student = Student.objects.get(id=student_id)
        room = HostelRoom.objects.get(id=room_id)

        student.room_assigned = room
        student.save()
        
        room.students_assigned += 1
        room.save()
        
        return redirect(f"/hostels/hostel-rooms/{room_id}/details/")
    return render(request, "hostels/rooms/add_student_to_room.html")


def remove_student_from_room(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        room_id = request.POST.get("room_id")
            
        student = Student.objects.get(id=student_id)
        room = HostelRoom.objects.get(id=room_id)

        student.room_assigned = None
        student.save()
        
        room.students_assigned -= 1
        room.save()
        
        return redirect(f"/hostels/hostel-rooms/{room_id}/details/")
    return render(request, "hostels/rooms/remove_student_from_room.html")