from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.username


class MyModel(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.phone
