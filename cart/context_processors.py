
def cart_summary(request):
    cart = request.session.get('cart', {})
    total_qty = sum(item['qty'] for item in cart.values())
    total_cost = sum(item['qty']*item['price'] for item in cart.values())
    return {'cart_total_qty': total_qty, 'cart_total_cost': total_cost}
