from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import Product


class ProductRegisterForm(UserCreationForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'photos']

        # Custom field label overrides
        labels = {'name': 'Nombre',
                  'description': 'Descripción',
                  'price': 'Precio',
                  'photos': 'Fotos'
        }
        
    # Description validator:
    # Description can't have more than 255 characters
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and (len(description)>255):
            raise forms.ValidationError('La descripción debe tener hasta 255 caracteres')    
        return description
    
    # Price validator:
    # The price can't be negative
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price<0 and price is not None:
            raise forms.ValidationError('El precio no puede ser negativo')
        return price
    
    # Name validator:
    # The product needs a name. It can't be empty
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if name is None:
            raise forms.ValidationError("El nombre del producto es obligatorio.")
        return name



