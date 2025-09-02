
from rest_framework import serializers

from .models import Cart, Cart_Items, Order, OrderItem
from .services import Order_Service
from flowers.models import Flowers

from django.core.mail import send_mail
from django.conf import settings



class Empty_Serializer( serializers.Serializer ):
    pass


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


# ______ Orders ________


class Create_Order_Serializer( serializers.Serializer ):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('Cart Not Found')
        
        if not Cart_Items.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart Is Empty')
        
        return cart_id
    
    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']

        try:
            order = Order_Service.create_order(user_id=user_id, cart_id=cart_id)

            user_email = order.user.email
            subject = "Order Confirmed"
            message = f"Hi {order.user.get_full_name()},\n\nYour order has been placed successfully!\nTotal: ${order.total_price}\n\nThank you for shopping with us!"
            
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [user_email],
                fail_silently=False,
            )

            return order
        except ValueError as e:
            return serializers.ValidationError(str(e))
        
    def to_representation(self, instance):
        return Order_Serializer(instance).data
    

class Order_Items_Serializer( serializers.ModelSerializer ):
    flower = Simplified_Flower_Serializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'flower', 'quantity', 'price', 'total_price']



class Update_Order_Serializer( serializers.ModelSerializer ):
    class Meta:
        model = Order
        fields = ['status']



class Order_Serializer( serializers.ModelSerializer ):
    items = Order_Items_Serializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'items']

