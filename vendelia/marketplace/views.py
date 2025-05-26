from django.shortcuts import render, redirect
from django.http import HttpRequest

from .forms import UserRegisterForm

# Constant imports
from .constants import GET, POST
from .constants import URL_PATH_INDEX, URL_NAME_INDEX
from .constants import URL_PATH_REGISTER_USER

# Marketplace app views

# Default index view
def index(request: HttpRequest):
    return render(
        request=request, 
        template_name=URL_PATH_INDEX
        )

# Register user view
def register_user(request: HttpRequest):
    # GET Request: Just show the user form
    if request.method == GET:
        register_user_form = UserRegisterForm()
        
        return render(
            request=request, 
            template_name=URL_PATH_REGISTER_USER,
            context={'register_user_form': register_user_form}
        )

    # POST Request: Process the user register form
    if request.method == POST:
        register_user_form = UserRegisterForm(request.POST)

        # If the form is valid, store new user and redirect to index
        if register_user_form.is_valid():
            # TODO verify+clean inputs
            new_user = register_user_form.save()
            return redirect(f'/{URL_NAME_INDEX}')
        
        # Otherwise, return to the register user form
        else:
            return render(
                request=request, 
                template_name=URL_PATH_REGISTER_USER,
                context={'register_user_form': register_user_form}
            )

def login_user(request):
    #Rendering of the template
    return render(request, 'marketplace/login_user.html')