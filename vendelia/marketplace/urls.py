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
from .constants import URL_NAME_USER_PROFILE, URL_PATTERN_USER_PROFILE

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
        name=URL_NAME_LOGIN
    ),
  
    # Product register form (new item to sell)
    path(
        route=URL_PATTERN_REGISTER_PRODUCT, 
        view=views.register_product, 
        name=URL_NAME_REGISTER_PRODUCT
    ),

    path(
        route=URL_PATTERN_SEARCH_PRODUCT, 
        view=views.search_product, 
        name=URL_NAME_SEARCH_PRODUCT
    ),
    # User profile
    path(
        route=URL_PATTERN_USER_PROFILE,
        view=views.user_profile,
        name=URL_NAME_USER_PROFILE
    ),

    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('', views.home, name='home'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('mis-compras/', views.mis_compras, name='mis_compras')
]
