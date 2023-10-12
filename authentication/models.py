from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """
    Модель Пользователь
    """
    password = models.TextField(max_length=50)
    first_name = models.TextField(max_length=50)
    last_name = models.TextField(max_length=50)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)
