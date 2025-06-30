from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import User, Product
import re

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            # Provided by AbstractUser
            'username',  'email',  'password1', 'password2', 

            # Provided by the custom User model
            'phone_number', 'first_name', 'last_name', 'city'
            ]
        
        # Custom field label overrides
        labels = {
            'username': 'Usuario',
            'email': 'Correo electrónico',
            'phone_number': 'Teléfono',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'city': 'Ciudad',
        }

    # Username validator
    # Length must be between 6 to 32 chars
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not (6 <= len(username) <= 32):
            raise forms.ValidationError('El nombre de usuario debe tener entre 6 y 32 caracteres.')
        
        return username
    
    # Phone number validator
    # Must be exactly 8 digits (only chilean cellphone numbers)
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if len(phone_number) != 8:
            raise forms.ValidationError('El número debe consistir de 8 dígitos.')
        elif not phone_number.isdigit():
            raise forms.ValidationError('El número debe consistir de solo dígitos.')
        
        return phone_number
    
    # City validator
    # Must be a string of length between 4 and 30.
    # 
    # Appropiate lenght taken from wikidata with this query:
    # SELECT ?item ?itemLabel (STRLEN(?itemLabel) AS ?labelLength) WHERE {
    # ?item wdt:P31 wd:Q25412763.
    # SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    # }
    def clean_city(self):
        city = self.cleaned_data.get('city')
        if len(city) < 4 or len(city) > 30:
            raise forms.ValidationError('La ciudad debe tener entre 4 a 30 caracteres.')
        if not city.isalpha():
            raise forms.ValidationError('La ciudad solo puede contener letras.')
        
        return city

      
class ProductRegisterForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'photos']

        # Custom field label overrides
        labels = {'product_name': 'Nombre',
                  'description': 'Descripción',
                  'price': 'Precio',
                  'photos': 'Fotos'
        }
    
    # Price validator
    # The price can't be negative
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price<0 and price is not None:
            raise forms.ValidationError('El precio no puede ser negativo')
        
        return price
    
    # Name validator
    # The name can't contain only empty spaces or the characters #, $ y %
    def clean_product_name(self):
        product_name = self.cleaned_data.get('product_name')
        if not product_name.strip():
            raise forms.ValidationError("El nombre no puede contener solo espacios")
        if re.search(r"[#$%]", product_name):
            raise forms.ValidationError("El nombre contiene caracteres no válidos (#, $, %)")
        return product_name
    
    # Description validator
    # The description can´t be made of only empty spaces
    # Also, the description can't have the folllowing characters: #, $ y %
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description.strip():
            raise forms.ValidationError("La descripción no puede sólo contener espacios en blanco")
        if re.search(r"[#$%]", description):
            raise forms.ValidationError("")
        return description


# Form to authenticate the user with email and password
class EmailAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Correo electrónico", max_length=254)
    password = forms.CharField(label="Contraseña", strip=False, widget=forms.PasswordInput)

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        clean_data = super().clean()
        email = clean_data.get('email')
        password = clean_data.get('password')

        if email and password:
            self.user = authenticate(request=self.request, username=email, password=password)
            if self.user is None:
                raise ValidationError("Correo o contraseña inválidos")
            
        return clean_data
    
    def get_user(self):
        return self.user
    