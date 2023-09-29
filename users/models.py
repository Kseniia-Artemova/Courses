from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для описания пользователя"""

    username = None

    email = models.EmailField(unique=True, verbose_name='E-mail')
    phone = models.CharField(null=True, blank=True, max_length=60, verbose_name='Телефон')
    city = models.CharField(null=True, blank=True, max_length=100, verbose_name='Город')
    avatar = models.ImageField(null=True, blank=True, upload_to='', verbose_name='Аватар')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []