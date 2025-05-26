from django.contrib import admin
from .models import User

# Register marketplace app models to admin panel
admin.site.register(User)
