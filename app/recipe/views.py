"""
Views for recipe APIs.
"""

from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe, Tag, Ingredient
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
        elif self.action == "upload_image":
            return serializers.RecipeImageSerializer

        return self.serializer_class

    # https://www.django-rest-framework.org/api-guide/generic-views/#get_serializer_classself
    def perform_create(self, serializer):
        """Create a new recipe."""
        serializer.save(user=self.request.user)

    @action(methods=["POST"], detail=True, url_path="upload-image")
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# TagViewSet ve IngredientViewSet için tekrar tekrar kullandığımızdan aynı kodları bu class ile tek yerde topluyoruz.
class BaseRecipeAttrViewSet(mixins.DestroyModelMixin,  # delete
                            mixins.UpdateModelMixin,  # update
                            mixins.ListModelMixin,
                            viewsets.GenericViewSet):
    """Base viewset for recipe attributes."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset to authenticad user."""
        return self.queryset.filter(user=self.request.user).order_by("-name")


class TagViewSet(BaseRecipeAttrViewSet):  # mixins, generic viewset'ten önce tanımlanmalı
    """Manage tags in the database."""
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()


class IngredientViewSet(BaseRecipeAttrViewSet):
    """Manage ingredients in the database."""
    serializer_class = serializers.IngredientSerializer
    queryset = Ingredient.objects.all()

