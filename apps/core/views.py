from django.shortcuts import render

from apps.students.models import Student, MealCard
from apps.staff.models import Staff
from apps.hostels.models import Booking


# Create your views here.
def home(request):
    students_count = Student.objects.count()
    staff_count = Staff.objects.count()
    meal_cards_count = MealCard.objects.count()
    bookings_count = Booking.objects.count()

    context = {
        "students_count": students_count,
        "staff_count": staff_count,
        "meal_cards_count": meal_cards_count,
        "bookings_count": bookings_count,
    }
    return render(request, "home.html", context)
