from django.db import models
from django.contrib.auth import get_user_model
from categorias.models import Categoria

# Create your models here.
User =  get_user_model()

# This model represents all the Products in Vendalia
# Fields:    name:           name of the product in the application (unique)
#            description:    text with a description of the product. Max length of 255 characters.
#            price:          price of the product in integers
#            photos:         pictures of the product
#            owner:          the user that owns the published product
#            categories:     name of the categories that classifiy the new product

class Product(models.Model):
    product_name = models.CharField(null=True)
    description = models.TextField(blank=True)
    price = models.IntegerField() 
    photos = models.ImageField(upload_to='product_images/', null=True, blank=True)

    #categories = models.ForeignKey(Categoria, default="general", on_delete=models.CASCADE)
    # Dejo esto pendiente para crear la carpeta con las categorias despues
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.name} - $ {self.price}"