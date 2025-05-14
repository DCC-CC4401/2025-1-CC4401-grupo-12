from django.shortcuts import render, redirect
from forms import ProductForm

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

