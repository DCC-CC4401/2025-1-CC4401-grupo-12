from django.shortcuts import render, redirect
from forms import ProductRegisterForm

# Create your views here.

#login required to do this
def register_product(request):
    if request.method == 'POST':
        form = ProductRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            product.save()
    else:
        form = ProductRegisterForm()

    return render(request, 'products/register_product.html', {'form': form})

