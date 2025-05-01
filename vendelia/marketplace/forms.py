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
