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
