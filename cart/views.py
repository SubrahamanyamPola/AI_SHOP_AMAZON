
from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from django.contrib import messages
def _cart(request):
    return request.session.setdefault('cart', {})
def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    for pid, it in cart.items():
        p = get_object_or_404(Product, id=int(pid))
        items.append({'product': p, 'qty': it['qty'], 'subtotal': it['qty']*it['price']})
    return render(request, 'cart/cart.html', {'items': items})
def cart_add(request, product_id):
    p = get_object_or_404(Product, id=product_id)
    cart = _cart(request); key = str(product_id)
    cart[key] = {'qty': cart.get(key, {'qty':0}).get('qty',0) + 1, 'price': float(p.price)}
    request.session.modified = True
    messages.success(request, f"Added {p.name} to cart.")
    return redirect('product_detail', slug=p.slug) if request.META.get('HTTP_REFERER') else redirect('cart_view')
def cart_remove(request, product_id):
    cart = _cart(request); cart.pop(str(product_id), None); request.session.modified = True
    return redirect('cart_view')
def cart_clear(request):
    request.session['cart'] = {}; request.session.modified = True
    return redirect('cart_view')
