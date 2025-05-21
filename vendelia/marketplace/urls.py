from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_product, name= 'register_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail')
]  