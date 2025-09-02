from django.db import models
from django.core.validators import MinValueValidator


class Category( models.Model ):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
    

class Flowers( models.Model ):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(validators=[MinValueValidator(1)])

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="flowers",
    )

    def __str__(self):
        return self.name
    

class Product_Images( models.Model ):
    # image = models.ImageField(upload_to="flowers/images/")

    flower = models.ForeignKey(
        Flowers,
        on_delete=models.CASCADE,
        related_name="images",
    )
