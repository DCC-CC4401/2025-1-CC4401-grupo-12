from django.db import models

# Create your models here.


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