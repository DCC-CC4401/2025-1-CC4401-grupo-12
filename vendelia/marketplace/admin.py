from django.contrib import admin
from .models import User, Categoria, Product

# Register marketplace app models to admin panel
admin.site.register(User)
admin.site.register(Categoria)
admin.site.register(Product)