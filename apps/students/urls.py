from django.urls import path
from apps.students.views import students, new_student, edit_student, delete_student, meal_cards, edit_mealcard, delete_mealcard

urlpatterns = [
    path("", students, name="students"),
    path("new-student/", new_student, name="new-student"),
    path("edit-student/", edit_student, name="edit-student"),
    path("delete-student/", delete_student, name="delete-student"),
    path("meal-cards/", meal_cards, name="meal-cards"),
    path("edit-mealcard/", edit_mealcard, name="edit-mealcard"),
    path("delete-mealcard/", delete_mealcard, name="delete-mealcard"),
]
