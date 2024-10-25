from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from django.db import transaction

from apps.staff.models import Staff, Department
from apps.users.models import User
from apps.core.models import UserRole
# Create your views here.
def staff(request):
    staff = Staff.objects.all().order_by("-created_on")
    
    paginator = Paginator(staff, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    user_roles = UserRole.objects.exclude(name__in=["Student", "Admin"]).all()
    departments = Department.objects.all()
        
    context = {
        "page_obj": page_obj,
        "user_roles": user_roles,
        "departments": departments
    }
    return render(request, "staff/staff.html", context)


@transaction.atomic
def new_staff(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        department = request.POST.get("department")
        role = request.POST.get("role")
        
        user_role = UserRole.objects.get(id=role)
        
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
            gender=gender
        )

        staff = Staff.objects.create(
            user=user,
            staff_number=phone_number,
            department_id=department
        )
        return redirect("staff")
    return render(request, "staff/new_staff.html")


@transaction.atomic
def edit_staff(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        gender = request.POST.get("gender")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        department = request.POST.get("department")
        role = request.POST.get("role")
        date_of_birth = request.POST.get("date_of_birth")
        
        staff = Staff.objects.get(id=staff_id)
        staff.user.first_name = first_name
        staff.user.last_name = last_name
        staff.user.email = email
        staff.user.role_id = role
        staff.user.phone_number = phone_number
        staff.user.address = address
        staff.user.city = city
        staff.user.country = country
        staff.user.gender = gender
        staff.user.date_of_birth = date_of_birth
        staff.user.save()
        
        staff.staff_number = phone_number
        staff.department_id = department
        staff.save()
        
        return redirect("staff")

    return render(request, "staff/edit_staff.html")
        
     
@transaction.atomic   
def delete_staff(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff_id")
        staff = Staff.objects.get(id=staff_id)
        
        staff.user.delete()
        staff.delete()
        return redirect("staff")
    return render(request, "staff/delete_staff.html")