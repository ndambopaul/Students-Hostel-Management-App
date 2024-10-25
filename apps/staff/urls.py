from django.urls import path
from apps.staff.views import staff, new_staff, edit_staff, delete_staff

urlpatterns = [
    path("", staff, name="staff"),
    path("new-staff/", new_staff, name="new-staff"),
    path("edit-staff/", edit_staff, name="edit-staff"),
    path("delete-staff/", delete_staff, name="delete-staff"),
]