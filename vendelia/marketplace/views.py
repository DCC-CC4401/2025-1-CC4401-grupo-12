from .models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import login
from django.contrib.staticfiles import finders
from django.core.files.base import File
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Product
from .forms import UserRegisterForm, ProductRegisterForm, EmailAuthenticationForm, ProductSearchForm
from .util import get_pagination_pages
from django.http import HttpResponseForbidden
from .decorators import bloquear_baneados

from .models import Product
from .models import Compra
from .forms import UserRegisterForm, ProductRegisterForm, EmailAuthenticationForm

# Constant imports
from .constants import GET, POST
from .constants import URL_PATH_INDEX, URL_NAME_INDEX
from .constants import URL_PATH_REGISTER_USER, URL_PATH_LOGIN, URL_PATH_SEARCH_PRODUCT
from .constants import PRODUCT_SEARCH_RESULTS_PER_PAGE

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
            return redirect('/')
        
        # Otherwise, return to the register user form
        else:
            return render(
                request=request, 
                template_name=URL_PATH_REGISTER_USER,
                context={'register_user_form': register_user_form}
            )

#login required to do this
def register_product(request):

    if request.user.is_authenticated and request.user.is_banned:
        return HttpResponseForbidden("Tu cuenta ha sido baneada. No puedes registrar productos.")

    if request.method == 'POST':
        form = ProductRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            
            # Assign owner if authenticated
            if request.user.is_authenticated:
                new_product.owner = request.user
                # new_product.save()

            # Add dummy image if no photos were uploaded
            if not new_product.photo1 and not new_product.photo2 and not new_product.photo3:
                dummy_image_path = finders.find('images/product_no_image.jpg')
                if dummy_image_path:
                    with open(dummy_image_path, 'rb') as fp:
                        new_product.photo1.save('dummy.jpg', File(fp), save=False)
                else:
                    raise Exception("No product dummy image not found in static files!")
                
            new_product.save()
            return redirect('home')
        
    else:
        form = ProductRegisterForm()

    return render(request, 'marketplace/register_product.html', {'form': form}) 


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'marketplace/product_detail.html', {'product': product})

#def home(request):
#    return render(request, 'marketplace/home.html')
 
def home(request):
    ciudad = request.GET.get('ciudad', '')
    
    if ciudad:
        productos = Product.objects.filter(owner__city__iexact=ciudad)
    else:
        productos = Product.objects.all()
    
    ciudades_disponibles = User.objects.values_list('city', flat=True).distinct()
    
    return render(request, 'marketplace/home.html', {
        'productos': productos,
        'ciudades': ciudades_disponibles,
        'ciudad_seleccionada': ciudad
    })
  
  
def login_user(request):
    # GET Request: Shows the login form to the user
    if request.method == GET:
        login_user_form = EmailAuthenticationForm()

        return render(
            request=request,
            template_name=URL_PATH_LOGIN,
            context={'login_user_form': login_user_form}
        )
    
    # POST Request: Process the user login form
    if request.method == POST:
        login_user_form = EmailAuthenticationForm(request=request, data=request.POST)

        # If the form is valid, redirects the user to index
        if login_user_form.is_valid():
            user = login_user_form.get_user()
            login(request, user)
            return redirect('/')
        # If not, return to the login user form
        else:
            return render(request, URL_PATH_LOGIN, {'login_user_form': login_user_form})
  
  
# Product search 
def search_product(request: HttpRequest):
    if request.method == GET:
        products = Product.objects.none()
        query = request.GET.get('query', '')

        if query:
            # Exact match/contained query in product name and description
            results_1 = Product.objects.filter(product_name__iexact=query)
            results_2 = Product.objects.filter(product_name__icontains=query)
            results_3 = Product.objects.filter(description__iexact=query)
            results_4 = Product.objects.filter(description__icontains=query)

            # Add results that contain any word of the query in the name or description
            query_words = query.strip().split(' ')
            results_5 = Product.objects.none()
            for word in query_words:
                results_5 |= Product.objects.filter(product_name__icontains=word)

            # Add results that contain any word of the query as its category
            results_6 = Product.objects.none()
            for word in query_words:
                results_6 = Product.objects.filter(category__name__icontains=word)

            # Combine unique results
            seen_ids = set()
            combined = []
            for query_set in [results_1, results_2, results_3, results_4, results_5, results_6]:
                for product in query_set:
                    if product.id not in seen_ids:
                        combined.append(product)
                        seen_ids.add(product.id)

            products = combined

        # Paginate results
        paginator = Paginator(products, PRODUCT_SEARCH_RESULTS_PER_PAGE)
        page = request.GET.get('page')

        try:
            products_page = paginator.page(page)
        except PageNotAnInteger:
            products_page = paginator.page(1)
        except EmptyPage:
            products_page = paginator.page(paginator.num_pages)

        # Generate pagination page numbers
        page_numbers = get_pagination_pages(products_page.number, paginator.num_pages)



        return render(
            request=request,
            template_name=URL_PATH_SEARCH_PRODUCT,
            context = {
                'query': query,
                'products': products_page,
                'page_numbers': page_numbers,
            }
        )

      
def mis_compras(request):
    if request.user.is_authenticated:
        if request.user.is_banned:
            return HttpResponseForbidden("Tu cuenta ha sido baneada. No puedes ver tus compras.")
        
        compras = Compra.objects.filter(comprador=request.user).select_related('producto')
        return render(request, 'marketplace/mis_compras.html', {'compras': compras})
    else:
        return redirect('login')  # o la URL que corresponda

