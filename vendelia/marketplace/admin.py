from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Categoria, Product, Compra

class UserAdmin(BaseUserAdmin):
    # Mostrar en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_banned')
    list_filter = ('is_staff', 'is_superuser', 'is_banned', 'is_active')
    
    # Campos que se pueden editar en la ficha del usuario
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Moderación', {'fields': ('is_banned',)}),
    )

    # Campos que aparecen al crear un nuevo usuario en el admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Moderación', {'fields': ('is_banned',)}),
    )

# Allow showing internal fields (creation_date)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'price', 'category', 'owner', 'is_sold', 'creation_date')
    readonly_fields = ('creation_date',)

# Register other marketplace app models to admin panel
admin.site.register(User)
admin.site.register(Categoria)
admin.site.register(Compra)
