
from rest_framework import serializers

from .models import Flowers, Category




class Flowers_Serializer( serializers.ModelSerializer ):
    class Meta:
        model = Flowers
        fields = ['id', 'name', 'category', 'price', 'stock', 'updated_at']


class Category_Serializer( serializers.ModelSerializer ):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']