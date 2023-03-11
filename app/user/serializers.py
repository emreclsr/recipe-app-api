"""
Serializers for the user API View.
"""
from django.contrib.auth import get_user_model

from rest_framework import serializers


# Serializer JSON onbjesini Python objesine dönüştürmeye yarar. Bununla birlikte rest framework bir çok özellik barındırdığından validasyon vb. işlemleri halledebilir.
class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]  # bu kısma kullanıcının API üzerinden değiştirebileceği field'lar veriliyor is_staff gibi alanlar buraya verilmemeli
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):  # Bu method validasyon hatasız tamamlandığında çağrılacaktır.
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)