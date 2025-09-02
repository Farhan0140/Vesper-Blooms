from rest_framework.exceptions import PermissionDenied, ValidationError

from django.db import transaction

from .models import Cart, Order, OrderItem


class Order_Service:
    @staticmethod
    def create_order(user_id, cart_id):
        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('flower').all()

            total_price = 0
            order_items = []

            for item in cart_items:
                flower = item.flower
                
                if flower.stock < item.quantity:
                    raise ValidationError({"detail": f"Not enough stock for {flower.name}. Available: {flower.stock}"})

                
                flower.stock -= item.quantity
                flower.save()

                total_price += item.quantity * flower.price

                order_items.append(
                    OrderItem(
                        order=None,  # will be assigned after order creation
                        flower=flower,
                        quantity=item.quantity,
                        price=flower.price,
                        total_price=flower.price * item.quantity,
                    )
                )

            
            order = Order.objects.create(user_id=user_id, total_price=total_price)

            
            for order_item in order_items:
                order_item.order = order

            OrderItem.objects.bulk_create(order_items)
            
            cart.delete()

            return order
        

    @staticmethod
    def cancel_order(order, user):
        if user.is_staff:
            order.status == Order.CANCELED
            order.save()
            return order
        
        if order.user != user:
            raise PermissionDenied({"detail": 'You Won\'t cancel others order'})
        
        if order.status == Order.DELIVERED:
            raise ValidationError({"detail": 'Your Order has been delivered now you can\'t cancel the order'})
        
        order.status = Order.CANCELED
        order.save()
        return order