from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

# Constant imports
from .constants import URL_PATTERN_INDEX, URL_NAME_INDEX
from .constants import URL_PATTERN_REGISTER_USER, URL_NAME_REGISTER_USER
from .constants import URL_PATTERN_LOGIN, URL_NAME_LOGIN

from .constants import URL_PATTERN_REGISTER_PRODUCT, URL_NAME_REGISTER_PRODUCT
from .constants import URL_PATTERN_SEARCH_PRODUCT, URL_NAME_SEARCH_PRODUCT
from .constants import URL_NAME_REGISTER_PRODUCT, URL_PATTERN_REGISTER_PRODUCT
from .constants import URL_PATTERN_MY_SALES, URL_NAME_MY_SALES
from .constants import URL_PATTERN_MY_PURCHASES, URL_NAME_MY_PURCHASES


# Register all marketplace URLS here
urlpatterns = [
    # Marketplace index
    path(
        route=URL_PATTERN_INDEX, 
        view=views.index, 
        name=URL_NAME_INDEX
    ),

    # User register form
    path(
        route=URL_PATTERN_REGISTER_USER, 
        view=views.register_user,
        name=URL_NAME_REGISTER_USER
    ),

    # User login form
    path(
        route=URL_PATTERN_LOGIN,
        view=views.login_user,
        name= URL_NAME_LOGIN
    ),
  
    # Product register form (new item to sell)
    path(
        route=URL_PATTERN_REGISTER_PRODUCT, 
        view=views.register_product, 
        name=URL_NAME_REGISTER_PRODUCT
    ),
    path(
        route=URL_PATTERN_MY_SALES,
        view=views.my_sales,
        name=URL_NAME_MY_SALES
    ),

    path(
        route=URL_PATTERN_MY_PURCHASES,
        view=views.my_purchases,
        name=URL_NAME_MY_PURCHASES
    ),

    path(
        route=URL_PATTERN_SEARCH_PRODUCT, 
        view=views.search_product, 
        name=URL_NAME_SEARCH_PRODUCT
    ),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(next_page=URL_PATTERN_LOGIN), name='logout'),
    path('comprar-producto/<int:product_id>/', views.buy_product, name='buy_product'),
    path('comprar-producto/<int:product_id>/', views.buy_product, name='buy_product'),
    path('mis-compras/', views.mis_compras, name='mis_compras')

]
