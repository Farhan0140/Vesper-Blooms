
from rest_framework import serializers

from .models import Cart, Cart_Items
from flowers.models import Flowers


class Simplified_Flower_Serializer( serializers.ModelSerializer ):
    class Meta:
        model = Flowers
        fields = ['id', 'name', 'price']


class Add_Cart_Items_Serializer( serializers.ModelSerializer ):
    flower_id = serializers.IntegerField()

    class Meta:
        model = Cart_Items
        fields = ['id', 'flower_id', 'quantity']

    def save(self, **kwargs):
        cart_id = self.context.get('cart_id')
        flower_id = self.validated_data.get('flower_id')
        quantity = self.validated_data.get('quantity')

        try:
            item = Cart_Items.objects.get(cart_id=cart_id, flower_id=flower_id)
            item.quantity += quantity
            self.instance = item.save()
        except Cart_Items.DoesNotExist:
            self.instance = Cart_Items.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance
    
    def validate_flower_id(self, attrs):
        if not Flowers.objects.filter(id=attrs).exists():
            raise serializers.ValidationError(f"Product not found with {attrs} id")
        return attrs
    

class Update_Cart_Item_Serializer( serializers.ModelSerializer ):
    class Meta:
        model = Cart_Items
        fields = ['quantity']



class Cart_Items_Serializer( serializers.ModelSerializer ):
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    flower = Simplified_Flower_Serializer()
    
    class Meta:
        model = Cart_Items
        fields = ['id', 'quantity', 'total_price', 'flower']
    
    def get_total_price(self, cart_items: Cart_Items):
        return cart_items.quantity * cart_items.flower.price


class Cart_Serializer( serializers.ModelSerializer ):
    items = Cart_Items_Serializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']

    def get_total_price(self, cart:Cart):
        return sum([ item.quantity * item.flower.price for item in cart.items.all()])
