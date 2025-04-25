from django.shortcuts import render


def wishlist(request):
    return render(request, 'store/wishlist.html')

def index(request):
    return render(request,'store/product_list.html')
# Create your views here.
from .models import Product

def product_list(request):
    products = Product.objects.all()
    return render(request, 'store\product_list.html', {'products': products})

# views.py
def orders_list(request):
    # You'll need an Order model later
    return render(request, 'store/orders_list.html')

# customer
def customers_list(request):
    return render(request, 'store/customers_list.html')
# views.py

def settings_page(request):
    return render(request, 'store/settings.html')


