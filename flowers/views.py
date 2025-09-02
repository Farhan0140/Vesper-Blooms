from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Flowers, Category
from .serializers import Flowers_Serializer, Category_Serializer
from .permissions import IS_Admin_ReadOnly


class Flowers_ViewSet( ModelViewSet ):
    queryset = Flowers.objects.all()
    serializer_class = Flowers_Serializer
    permission_classes = [IS_Admin_ReadOnly]


class Category_ViewSet( ModelViewSet ):
    queryset = Category.objects.all()
    serializer_class = Category_Serializer
    permission_classes = [IS_Admin_ReadOnly]

