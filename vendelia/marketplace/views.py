from django.shortcuts import render, redirect, get_object_or_404
from forms import ProductForm
from models import Product
# Create your views here.

def register_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_view') #tengo q ver esto
    else:
        form = ProductForm()
    return render(request, 'register_product.html', {'form': form})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product_detail.html', {'product': product})
