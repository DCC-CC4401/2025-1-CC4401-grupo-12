from django.db import models
from django.contrib.auth import get_user_model
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


# Model that represents every product category
# Work in progress
class Categoria(models.Model):
    name = models.CharField(max_length=254)

    
# This model represents all the Products in Vendalia
# Fields:    name:           name of the product in the application (unique)
#            description:    text with a description of the product. Max length of 255 characters.
#            price:          price of the product in integers
#            photo1:         picture 1 of the product
#            photo2:         picture 2 of the product
#            photo3:         picture 3 of the product
#            owner:          the user that owns the published product
#            categories:     name of the categories that classifiy the new product (work in progress)
class Product(models.Model):
    product_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255, blank=True)
    price = models.IntegerField() 
    photo1 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    photo2 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    photo3 = models.ImageField(upload_to='product_images/', null=True, blank=True)
    #category = models.ForeignKey(Categoria, default="general", on_delete=models.CASCADE)
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.product_name} - $ {self.price}"
