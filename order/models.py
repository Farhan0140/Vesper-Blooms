from django.db import models
from django.core.validators import MinValueValidator
from uuid import uuid4

from users.models import User
from flowers.models import Flowers



class Cart( models.Model ):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
    )

    def __str__(self):
        return f"Cart of {self.user.get_full_name()}"


class Cart_Items( models.Model ):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )

    flower = models.ForeignKey(
        Flowers,
        on_delete=models.CASCADE,
    )
    
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'flower']]  

    def __str__(self):
        return f"{self.flower} --> {self.quantity}"


class Order(models.Model):
    NOT_PAID = 'Not Paid'
    PENDING = 'Pending'
    READY_TO_SHIP = 'Ready To Ship'
    SHIPPED = 'Shipped'
    DELIVERED = 'Delivered'
    CANCELED = 'Canceled'
    STATUS_CHOICES = [
        (NOT_PAID, 'Not Paid'),
        (READY_TO_SHIP, 'Ready To Ship'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELED, 'Canceled'),
        (PENDING, 'Pending')
    ]

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="orders"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order by {self.user.first_name} {self.user.last_name} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, 
        on_delete=models.CASCADE, 
        related_name="items"
    )

    flower = models.ForeignKey(Flowers, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.flower.name}"
    