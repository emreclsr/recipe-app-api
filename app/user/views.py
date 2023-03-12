"""
Views for the user API.
"""
from rest_framework import generics  # db'de object oluşturmaya yaramaktadır.
from rest_framework.authtoken.views import ObtainAuthToken  # Token oluşturmak için rest framework tarafından sağlanan view
from rest_framework.settings import api_settings  # Token oluşturma işi için eklendi

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
    )


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES