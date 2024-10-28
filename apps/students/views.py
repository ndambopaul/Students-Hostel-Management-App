from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages

from apps.students.models import Student, StudentDocument, MealCard
from apps.users.models import User
from apps.core.models import UserRole

months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


GENDER_CHOICES = ["Male", "Female"]


# Create your views here.
def students(request):
    students = Student.objects.all().order_by("-created_on")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        if search_text:
            students = Student.objects.filter(
                Q(user__first_name__icontains=search_text)
                | Q(user__last_name__icontains=search_text)
                | Q(registration_number__icontains=search_text)
            )

    paginator = Paginator(students, 8)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "gender_choices": GENDER_CHOICES}
    return render(request, "students/students.html", context)


def student_details(request, id):
    student = Student.objects.get(id=id)

    context = {"student": student}
    return render(request, "students/student_details.html", context)


def new_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        registration_number = request.POST.get("registration_number")
        guardian_name = request.POST.get("guardian_name")
        guardian_phone_number = request.POST.get("guardian_phone_number")
        date_of_birth = request.POST.get("date_of_birth")

        user_role = UserRole.objects.get(name="Student")

        print(f"Gender: {gender}")

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=email,
            role=user_role,
            phone_number=phone_number,
            address=address,
            city=city,
            country=country,
            gender=gender,
            date_of_birth=date_of_birth,
        )

        student = Student.objects.create(
            user=user,
            registration_number=registration_number,
            guardian_name=guardian_name,
            guardian_phone_number=guardian_phone_number,
            status="Active",
        )
        messages.success(request, "Student created successfully.")
        return redirect("students")
    return render(request, "students/new_student.html")


def edit_student(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        registration_number = request.POST.get("registration_number")
        guardian_name = request.POST.get("guardian_name")
        guardian_phone_number = request.POST.get("guardian_phone_number")
        student_id = request.POST.get("student_id")
        date_of_birth = request.POST.get("date_of_birth")

        user_role = UserRole.objects.get(name="Student")

        student = Student.objects.get(id=student_id)

        student.user.first_name = first_name
        student.user.last_name = last_name
        student.user.email = email
        student.user.phone_number = phone_number
        student.user.address = address
        student.user.city = city
        student.user.country = country
        student.user.gender = gender
        student.user.date_of_birth = date_of_birth
        student.user.save()

        student.registration_number = registration_number
        student.guardian_name = guardian_name
        student.guardian_phone_number = guardian_phone_number
        student.save()
        messages.success(request, "Student updated successfully.")
        return redirect("students")
    return render(request, "students/edit_student.html")


def delete_student(request):
    if request.method == "POST":
        student_id = request.POST.get("student_id")
        student = Student.objects.get(id=student_id)
        student.user.delete()
        student.delete()
        return redirect("students")
    return render(request, "students/delete_student.html")


def meal_cards(request):
    meal_cards = MealCard.objects.all().order_by("-created_on")

    paginator = Paginator(meal_cards, 7)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "months": months}
    return render(request, "mealcards/mealcards.html", context)


def edit_mealcard(request):
    if request.method == "POST":
        mealcard_id = request.POST.get("mealcard_id")
        expiry_date = request.POST.get("expiry_date")
        card_number = request.POST.get("card_number")
        month = request.POST.get("month")
        year = request.POST.get("year")

        mealcard = MealCard.objects.get(id=mealcard_id)
        mealcard.expiry_date = expiry_date
        mealcard.card_number = card_number
        mealcard.month = month
        mealcard.year = year
        mealcard.save()

        return redirect("meal-cards")

    return render(request, "mealcards/edit_mealcard.html")


def delete_mealcard(request):
    if request.method == "POST":
        mealcard_id = request.POST.get("mealcard_id")
        mealcard = MealCard.objects.get(id=mealcard_id)
        mealcard.delete()
        return redirect("meal-cards")

    return render(request, "mealcards/delete_mealcard.html")



def checkin_students(request):
    students = Student.objects.filter(status="Pending Check-In").order_by("-created_on")

    if request.method == "POST":
        search_text = request.POST.get("search_text")
        if search_text:
            students = Student.objects.filter(
                Q(user__first_name__icontains=search_text)
                | Q(user__last_name__icontains=search_text)
                | Q(registration_number__icontains=search_text)
            ).filter(status="Pending Check-In").order_by("-created_on")

    paginator = Paginator(students, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "gender_choices": GENDER_CHOICES}
    return render(request, "students/checkin_out/checkin_students.html", context)