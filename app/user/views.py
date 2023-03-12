"""
Views for the user API.
"""
from rest_framework import (generics,  # db'de object oluşturmaya yaramaktadır.
                            authentication,
                            permissions,
                           )
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


class ManageUserView(generics.RetrieveUpdateAPIView):  # RetrieveUpdateAPIView rest framework tarafından databaseden obje getirmek ve update etmek için kullanılmaktadır.
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):  # Bu url'e ("me") get request'i geldiğinde bu method çalışacaktır.
        """Retrieve and return the authenticated user."""
        return self.request.user