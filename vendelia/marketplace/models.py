from django.db import models
from django.contrib.auth.models import AbstractUser


# This model represents all the Users in Vendelia
# It also has: username, password and email fields, given by its parent class.
class User(AbstractUser):
    phone_number = models.CharField(max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
