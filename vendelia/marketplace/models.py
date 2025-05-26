from django.db import models
from django.contrib.auth.models import AbstractUser


# This model represents all the Users in Vendelia
# Fields:   username:       name of the user in the application (unique)
#           email:          email address of the user in the application (unique)
#           phone_number:   phone number of the user (unique)
#           first_name:     first name of their real name, used for contact purposes after sales.
#           last_name:      last name of their real name, ditto.
#           city:           the city of residence of the user.
class User(AbstractUser):
    # AbstractUser overrides:
    #   username: max length
    #   email: max length, must be unique
    username = models.CharField(max_length=32, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    
    phone_number = models.CharField(max_length=8, unique=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    city = models.CharField(max_length=32)
