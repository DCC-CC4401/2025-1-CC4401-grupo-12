from django.db import models
from django.contrib.auth.models import AbstractUser


# This model represents all the Users in Vendelia
# It also has: username, password and email fields, given by its parent class.
class User(AbstractUser):
    # AbstractUser overrides:
    #   username: max length
    #   email: max length, must be unique
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    
    phone_number = models.CharField(max_length=8)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
