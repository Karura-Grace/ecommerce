from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Product, Category, Customer, Order, WishlistItem


# ── Product List / Home ──────────────────────────────────────────────────────

def product_list(request):
    products = Product.objects.select_related('category').all()
    categories = Category.objects.all()

    # Search
    query = request.GET.get('q', '').strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Category filter
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Sort
    sort = request.GET.get('sort', '')
    sort_map = {
        'price_asc': 'price',
        'price_desc': '-price',
        'newest': '-created_at',
    }
    if sort in sort_map:
        products = products.order_by(sort_map[sort])

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category_id,
        'selected_sort': sort,
    })


# ── Product Detail ───────────────────────────────────────────────────────────

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    related = Product.objects.filter(category=product.category).exclude(pk=pk)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related': related,
    })


# ── Cart ─────────────────────────────────────────────────────────────────────

def cart_detail(request):
    cart = request.session.get('cart', {})
    items = []
    total = 0
    for product_id, qty in cart.items():
        try:
            product = Product.objects.get(pk=int(product_id))
            subtotal = product.price * qty
            total += subtotal
            items.append({'product': product, 'quantity': qty, 'subtotal': subtotal})
        except Product.DoesNotExist:
            pass
    return render(request, 'store/cart.html', {'items': items, 'total': total})


def cart_add(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = request.session.get('cart', {})
    key = str(pk)
    cart[key] = cart.get(key, 0) + 1
    request.session['cart'] = cart
    messages.success(request, f'"{product.name}" added to cart.')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


def cart_remove(request, pk):
    cart = request.session.get('cart', {})
    cart.pop(str(pk), None)
    request.session['cart'] = cart
    return redirect('cart_detail')


def cart_update(request, pk):
    if request.method == 'POST':
        qty = int(request.POST.get('quantity', 1))
        cart = request.session.get('cart', {})
        if qty > 0:
            cart[str(pk)] = qty
        else:
            cart.pop(str(pk), None)
        request.session['cart'] = cart
    return redirect('cart_detail')


# ── Orders ───────────────────────────────────────────────────────────────────

@login_required
def orders_list(request):
    try:
        customer = request.user.customer
        orders = Order.objects.filter(customer=customer).prefetch_related('orderitem_set__product')
    except Customer.DoesNotExist:
        orders = []
    return render(request, 'store/orders_list.html', {'orders': orders})


# ── Customers (admin-style view) ─────────────────────────────────────────────

@login_required
def customers_list(request):
    if not request.user.is_staff:
        return redirect('product_list')
    customers = Customer.objects.select_related('user').all()
    return render(request, 'store/customers_list.html', {
        'customers': customers,
        'total_customers': customers.count(),
    })


# ── Wishlist ─────────────────────────────────────────────────────────────────

@login_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product')
    return render(request, 'store/wishlist.html', {'items': items})


@login_required
def wishlist_toggle(request, pk):
    product = get_object_or_404(Product, pk=pk)
    obj, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        obj.delete()
        messages.info(request, f'"{product.name}" removed from wishlist.')
    else:
        messages.success(request, f'"{product.name}" added to wishlist.')
    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


# ── Settings ─────────────────────────────────────────────────────────────────

@login_required
def settings_page(request):
    return render(request, 'store/settings.html')
