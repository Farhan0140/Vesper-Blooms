from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager


class User( AbstractUser ):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        full_name = f"{self.first_name} {self.last_name}"
        full_name = self.get_full_name()
        if full_name:
            return full_name

        return self.email 