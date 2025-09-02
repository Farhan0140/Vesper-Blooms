from django.contrib import admin

from .models import Flowers, Category, Flower_Images


admin.site.register(Flowers)
admin.site.register(Flower_Images)
admin.site.register(Category)
