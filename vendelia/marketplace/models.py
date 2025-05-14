from django.db import models

# Create your models here.


# This model represents all the Products in Vendalia
# Fields:    name:           name of the product in the application (unique)
#            description:    text with a description of the product. Max length of 255 characters.
#            price:          price of the product in integers
#            photos:         pictures of the product
#

class Product(models.Model):

    name = models.CharField()
    description = models.TextField() #Chequear con el equipo
    price = models.IntegerField() 
    photos = models.ImageField(upload_to='')
    
    def __str__(self):
        return self.name