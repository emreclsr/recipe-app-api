"""
Views for recipe APIs.
"""

from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):  # ModelViewSet -> modelleri ile çalışmka için kullanışlıdır. get, post, put, patch, ... methodlarını barındırır
    """View for manage recipe APIs."""
    serializer_class = serializers.RecipeDetailSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):  # Normalde queryset içindeki get tüm recipe'leri dönerdi fakat burada o methodu overwrite ederek user'a ait recipe'lerin gelmesini sağlayacak şekilde düzenliyoruz.
        """Retrieve recipes for authenticated user."""
        return self.queryset.filter(user=self.request.user).order_by("-id")

    # https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
    def get_serializer_class(self):  # burada serialize class'ı çağırmayı overwrite ediyoruz. eğer list aksiyonu olursa RecipeSerializer eğer diğer bir aksiyon ise RecipeDetailSerializer dönmesini sağlayacak şekilde düzenliyoruz. Bu işlemi RecipeSerializer için yazdığımız kısımları RecipeDetailSerializer için tekrar yazmamak için yapıyoruz.
        """Return the serializer class for request."""
        if self.action == "list":
            return serializers.RecipeSerializer

        return self.serializer_class

    # https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)


class TagViewSet(mixins.DestroyModelMixin,  # delete
                 mixins.UpdateModelMixin,  # update
                 mixins.ListModelMixin,
                 viewsets.GenericViewSet):  # mixins, generic viewset'ten önce tanımlanmalı
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticad user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")

