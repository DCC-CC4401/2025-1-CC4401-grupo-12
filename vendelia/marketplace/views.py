from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.utils import timezone
from django.contrib.staticfiles import finders
from django.core.files.base import File
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.utils import timezone


from .models import Product, Compra, User
from .forms import UserRegisterForm, ProductRegisterForm, EmailAuthenticationForm, ProductSearchForm, ProductEditForm
from .util import get_pagination_pages, get_all_categories
from django.http import HttpResponseForbidden
from .decorators import bloquear_baneados


# Constant imports
from .constants import GET, POST
from .constants import URL_PATH_REGISTER_USER, URL_PATH_LOGIN, URL_PATH_SEARCH_PRODUCT, URL_PATH_USER_PROFILE
from .constants import PRODUCT_SEARCH_RESULTS_PER_PAGE, PRODUCT_LIST_IN_HOME_PAGE

# Marketplace app views

# Register user view
def register_user(request: HttpRequest):
    # GET Request: Just show the user form
    if request.method == GET:
        register_user_form = UserRegisterForm()
        
        return render(
            request=request, 
            template_name=URL_PATH_REGISTER_USER,
            context={
                'register_user_form': register_user_form,
                'product_search_form': ProductSearchForm(),
                'categories': get_all_categories(),
                }
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
                context={
                    'register_user_form': register_user_form,
                    'product_search_form': ProductSearchForm(),
                    'categories': get_all_categories(),
                    }
            )

# View to Register a new product in the marketplace
@login_required(login_url='/login/')
def register_product(request):
    if request.user.is_banned:
        return HttpResponseForbidden("Tu cuenta ha sido suspendida. No puedes publicar nuevos avisos.")

    if request.method == 'POST':
        form = ProductRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.owner = request.user

            # Add dummy image if no photos were uploaded
            if not new_product.photo1 and not new_product.photo2 and not new_product.photo3:
                dummy_image_path = finders.find('images/product_no_image.jpg')
                if dummy_image_path:
                    with open(dummy_image_path, 'rb') as fp:
                        new_product.photo1.save('dummy.jpg', File(fp), save=False)
                else:
                    raise Exception("No product dummy image not found in static files!")
                
            new_product.save()
            return redirect('my_sales')
        
    else:
        form = ProductRegisterForm()

    return render(
        request=request, 
        template_name='marketplace/register_product.html', 
        context={
            'form': form,
            'product_search_form': ProductSearchForm(),
            'categories': get_all_categories(),
            }
        ) 

# Deprecated, see above
# View to register a product into the market
# @login_required(login_url='/login/')
# def register_product(request):
#     if request.method == 'POST':
#         form = ProductRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_product = form.save(commit=False)
#             new_product.owner = request.user
#             new_product.save()  # Save only after ypou press the button
#             # Redirect to my-sales to prevent duplicate submissions
#             return redirect('my_sales')
#     else:
#         form = ProductRegisterForm()

#     return render(request, 'marketplace/register_product.html', {'form': form})

# View to see details about the product
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    return render(
        request=request, 
        template_name='marketplace/product_detail.html', 
        context={
            'product': product,
            'product_search_form': ProductSearchForm(),
            'categories': get_all_categories(),
            }
        )

# Home view, landing page + latest products
def home(request):
    if request.method == GET:
        # Home view should not have filtering capacities, these are supposed to go in the search/explore page
        # ciudad = request.GET.get('ciudad', '')
        # if ciudad:
        #     productos = Product.objects.filter(owner__city__iexact=ciudad)
        # else:
        #     productos = Product.objects.all()
        
        # ciudades_disponibles = User.objects.values_list('city', flat=True).distinct()

        search_bar = ProductSearchForm()
        products = Product.objects.filter(is_sold=False).order_by('-creation_date')[:PRODUCT_LIST_IN_HOME_PAGE]
        
        return render(request, 'marketplace/home.html', {
            'product_search_form': search_bar,
            'products': products,
            'categories': get_all_categories(),
        })
  

# View that handles user login
def login_user(request):
    # GET Request: Shows the login form to the user
    if request.method == GET:
        login_user_form = EmailAuthenticationForm()

        return render(
            request=request,
            template_name=URL_PATH_LOGIN,
            context={
                'login_user_form': login_user_form,
                'product_search_form': ProductSearchForm(),
                'categories': get_all_categories(),
                }
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
            return render(
                request=request, 
                template_name=URL_PATH_LOGIN, 
                context={
                    'login_user_form': login_user_form,
                    'product_search_form': ProductSearchForm(),
                    'categories': get_all_categories(), 
                    }
                )
  

# View to see all the current sales for the user
@login_required(login_url='/login/')
def my_sales(request):
    user_products = Product.objects.filter(owner=request.user)
    # Separate active listings from sold items
    active_listings = user_products.filter(is_sold=False)
    sold_items = user_products.filter(is_sold=True)
    
    context = {
        'active_listings': active_listings,
        'sold_items': sold_items,
        'active_count': active_listings.count(),
        'sold_count': sold_items.count(),

        'product_search_form': ProductSearchForm(),
        'categories': get_all_categories(),

    }
    
    return render(
        request=request, 
        template_name='marketplace/my_sales.html', 
        context=context
        )

# View that shows all the products that the user has bought
@login_required(login_url='/login/')
def my_purchases(request):
    # Obtener todos los productos que el usuario ha comprado
    purchased_items = Product.objects.filter(sold_to=request.user, is_sold=True)
    
    context = {
        'purchased_items': purchased_items,
        'purchased_count': purchased_items.count(),
        
        'product_search_form': ProductSearchForm(),
        'categories': get_all_categories(),
    }
    
    return render(request, 'marketplace/my_purchases.html', context)


# View used to buy a product
@login_required(login_url='/login/')
def buy_product(request, product_id):
    if request.method == 'POST':
        try:
            product = get_object_or_404(Product, id=product_id, is_sold=False)
            
            # Verificar que el usuario no esté comprando su propio producto
            if product.owner == request.user:
                return JsonResponse({
                    'success': False,
                    'message': 'No puedes comprar tu propio producto.'
                })
            
            # Marcar como vendido y asignar comprador
            product.is_sold = True
            product.sold_to = request.user
            product.date_sold = timezone.now()
            product.save()
            
            return JsonResponse({
                'success': True,
                'message': '¡Producto comprado exitosamente!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': 'Error al comprar el producto.'
            })
    
    return JsonResponse({'success': False, 'message': 'Método de solicitud inválido.'})

  
# View for product search, provides a query based on several parameters
def search_product(request: HttpRequest):
    if request.method == GET:
        products = Product.objects.none()
        query = request.GET.get('query', '')
        mode = request.GET.get('mode', 'all')

        if query:
            if mode == 'all':
                # Exact match/contained query in product name and description
                results_1 = Product.objects.filter(product_name__iexact=query, is_sold=False)
                results_2 = Product.objects.filter(product_name__icontains=query, is_sold=False)
                results_3 = Product.objects.filter(description__iexact=query, is_sold=False)
                results_4 = Product.objects.filter(description__icontains=query, is_sold=False)

                # Add results that contain any word of the query in the name or description
                query_words = query.strip().split(' ')
                results_5 = Product.objects.none()
                for word in query_words:
                    results_5 |= Product.objects.filter(product_name__icontains=word, is_sold=False)

                # Add results that contain any word of the query as its category
                results_6 = Product.objects.none()
                for word in query_words:
                    results_6 = Product.objects.filter(category__name__icontains=word, is_sold=False)

                # Combine unique results
                seen_ids = set()
                combined = []
                for query_set in [results_1, results_2, results_3, results_4, results_5, results_6]:
                    for product in query_set:
                        if product.id not in seen_ids:
                            combined.append(product)
                            seen_ids.add(product.id)

                products = combined

            elif mode == 'category':
                products = Product.objects.filter(category__name__icontains=query)

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

                'product_search_form': ProductSearchForm(),
                'categories': get_all_categories(),
            }
        )

# Deprecated view, see my_purchases
# def mis_compras(request):
#     if request.user.is_authenticated:
#         if request.user.is_banned:
#             return HttpResponseForbidden("Tu cuenta ha sido baneada. No puedes ver tus compras.")
        
#         compras = Compra.objects.filter(comprador=request.user).select_related('producto')
#         return render(
#             request=request, 
#             template_name='marketplace/mis_compras.html', 
#             context={
#                 'compras': compras,
#                 'product_search_form': ProductSearchForm(),
#                 'categories': get_all_categories(), 
#                 }
#             )
#     else:
#         return redirect('login')  # o la URL que corresponda

# View to mark a product as sold
def mark_as_sold(request, product_id):
    print(product_id)
    # Allow only POST requests
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    # Check if user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseForbidden('Authentication required')

    product = get_object_or_404(Product, id=product_id, owner=request.user)

    if getattr(product, 'is_sold', False):
        return JsonResponse({'success': False, 'message': 'El producto ya está vendido.'})

    product.is_sold = True
    product.date_sold = timezone.now()
    product.save()

    return JsonResponse({'success': True})

@login_required(login_url='/login/')
def edit_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, owner=request.user)
    
    if request.user != product.owner:
        return HttpResponseForbidden('You don´t have permission to edit this product')
    
    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product.save()  # Save on+ly after ypou press the button
            # Redirect to my-sales to prevent duplicate submissions
            return redirect('product_detail', product_id=product_id)
    else:
        form = ProductEditForm(instance=product)

    return render(request, 'marketplace/edit_product.html', {'form': form, 'product': product})

@login_required(login_url='/login/')
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, owner=request.user)
    product.delete()
    
    return redirect('my_sales')

# User profile
@login_required(login_url='/login/')
def user_profile(request):
    return render(
        request=request,
        template_name=URL_PATH_USER_PROFILE,
        context= {
            'user': request.user
        }
    )