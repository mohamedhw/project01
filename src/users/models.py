from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=13) 
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username