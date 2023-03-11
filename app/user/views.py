"""
Views for the user API.
"""
from rest_framework import generics  # db'de object oluşturmaya yaramaktadır.

from user.serializers import UserSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer