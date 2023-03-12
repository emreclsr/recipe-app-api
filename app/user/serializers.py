"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as _

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

    def update(self, instance, validated_data):  # update method'unu override ettik
        """Update and return user."""
        password = validated_data.pop("password", None)  # Kullanıcı örneğin email değiştirirken, şifre girmesini istemeyebiliriz bu nedenle password field'ını validasyon'dan çıkarıyoruz.
        user = super().update(instance, validated_data)  # super ile ModelSerializer içerindeki update'i tekrar çağırıyoruz. Üst satırda gereken düzeltmeyi yapıp tekrar base modelin update method'unu kullanıyoruz.

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):  # attrs: Attributes
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )

        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="autherization")

        attrs["user"] = user
        return attrs
