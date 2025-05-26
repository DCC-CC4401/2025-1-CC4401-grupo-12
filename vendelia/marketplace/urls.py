from django.urls import path
from . import views

# Constant imports
from .constants import URL_PATTERN_INDEX, URL_NAME_INDEX
from .constants import URL_PATTERN_REGISTER_USER, URL_NAME_REGISTER_USER
from .constants import URL_PATTERN_LOGIN, URL_NAME_LOGIN

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
    #- User login form
    path(
        route=URL_PATTERN_LOGIN,
        view=views.login_user,
        name= URL_NAME_LOGIN
    ),
]
