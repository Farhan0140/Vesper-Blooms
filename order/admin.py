from django.contrib import admin

from .models import Cart, Cart_Items


@admin.register(Cart)
class Cart_Admin( admin.ModelAdmin ):
    list_display = ['id', 'user']


admin.site.register(Cart_Items)
