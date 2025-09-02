from django.contrib import admin

from .models import Cart, Cart_Items, Order, OrderItem


@admin.register(Cart)
class Cart_Admin( admin.ModelAdmin ):
    list_display = ['id', 'user']


@admin.register(Order)
class Order_Admin( admin.ModelAdmin ):
    list_display = ['id', 'user', 'status']


admin.site.register(Cart_Items)
admin.site.register(OrderItem)
