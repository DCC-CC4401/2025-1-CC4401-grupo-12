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

    
# This model represents all the Products in Vendalia
# Fields:    name:           name of the product in the application (unique)
#            description:    text with a description of the product. Max length of 255 characters.
#            price:          price of the product in integers
#            photos:         pictures of the product
#

class Product(models.Model):

    name = models.CharField(max_length=250)                                               # Varchar
    description = models.TextField(blank=True)                                            # Chequear con el equipo
    price = models.IntegerField(max_digits=10)                                            # Max. price 9.999.999.999
    photos = models.ImageField(upload_to='')                                              # Image to show the product
    category = models.ForeignKey(Categoria, default="general", on_delete=models.CASCADE)  # Foreign key (hay que crear categorias)

    def __str__(self):
        return self.name                                                                  # Name to be shown when called
