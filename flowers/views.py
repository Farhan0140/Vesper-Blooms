from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet

from .models import Flowers, Category, Flower_Images
from .serializers import Flowers_Serializer, Category_Serializer, Flower_Image_Serializer
from .permissions import IS_Admin_ReadOnly


class Flowers_ViewSet( ModelViewSet ):
    queryset = Flowers.objects.all()
    serializer_class = Flowers_Serializer
    permission_classes = [IS_Admin_ReadOnly]


class Category_ViewSet( ModelViewSet ):
    queryset = Category.objects.all()
    serializer_class = Category_Serializer
    permission_classes = [IS_Admin_ReadOnly]


class Flower_Images_ViewSet( ModelViewSet ):
    serializer_class = Flower_Image_Serializer
    permission_classes = [IS_Admin_ReadOnly]


    def get_queryset(self):
        return Flower_Images.objects.filter(flower_id=self.kwargs.get('flower_pk'))
    
    def perform_create(self, serializer):
        serializer.save(flower_id=self.kwargs.get('flower_pk'))

