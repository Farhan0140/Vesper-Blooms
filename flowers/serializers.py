
from rest_framework import serializers

from .models import Flowers, Category, Flower_Images



class Flower_Image_Serializer( serializers.ModelSerializer ):
    image = serializers.ImageField()
    
    class Meta:
        model = Flower_Images
        fields = ['id', 'image']


class Flowers_Serializer( serializers.ModelSerializer ):
    images = Flower_Image_Serializer(read_only=True, many=True)

    class Meta:
        model = Flowers
        fields = ['id', 'name', 'category', 'price', 'stock', 'updated_at', 'images']


class Category_Serializer( serializers.ModelSerializer ):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']