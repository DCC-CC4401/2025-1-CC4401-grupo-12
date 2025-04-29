from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            # Provided by AbstractUser
            'username',  'email',  'password1', 'password2', 

            # Provided by the custom User model
            'phone_number', 'first_name', 'last_name'
            ]
        
        # Custom field label overrides
        labels = {
            'phone_number': 'Teléfono',
            'first_name': 'Nombre',
            'last_name': 'Apellido'
        }
