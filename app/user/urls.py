"""
URL mappings for the user API.
"""
from django.urls import path

from user import views

app_name = "user"  # test'te yer alan reverse("user:create")'daki user burada tanımlanmaktadır.

urlpatterns = [
    path("create/", views.CreateUserView.as_view(), name="create"),
]