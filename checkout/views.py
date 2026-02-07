from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render

from shop.models import Product
from .forms import AddressForm
from .models import Order, OrderItem


def _get_cart(request):
    """Cart is stored in session as {product_id: {qty, price}}."""
    return request.session.get("cart", {}) or {}


def _cart_total(cart: dict) -> float:
    return float(sum(item["qty"] * item["price"] for item in cart.values()))


def address(request):
    cart = _get_cart(request)
    if not cart:
        return redirect("cart_view")

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            request.session["shipping"] = form.cleaned_data
            request.session.modified = True
            return redirect("checkout_payment")
    else:
        form = AddressForm()

    return render(request, "checkout/address.html", {"form": form})


@transaction.atomic
def payment(request):
    """
    Payment page for Revolut.Me flow:
    - Create an Order once (PENDING) and create OrderItems
    - User clicks "Pay with Revolut" (opens revolut.me)
    - User returns and clicks "I have paid" -> status PAYMENT_SUBMITTED
    """
    cart = _get_cart(request)
    ship = request.session.get("shipping")

    if not cart:
        return redirect("cart_view")
    if not ship:
        return redirect("checkout_address")

    # Create the order only once per session shipping/cart
    order_id = request.session.get("checkout_order_id")
    order = Order.objects.filter(id=order_id).first() if order_id else None

    if not order:
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=ship.get("full_name") or ship.get("name") or "",
            email=ship.get("email") or "",
            address=ship.get("address") or "",
            city=ship.get("city") or "",
            country=ship.get("country") or "",
            payment_provider="revolut",
            payment_status="PENDING",
        )

        for pid, item in cart.items():
            p = get_object_or_404(Product, id=int(pid))
            OrderItem.objects.create(
                order=order,
                product_name=getattr(p, "name", str(p)),
                price=p.price,
                quantity=item["qty"],
            )

        request.session["checkout_order_id"] = order.id
        request.session.modified = True

    cart_total_cost = _cart_total(cart)

    if request.method == "POST":
        # User confirms they paid via Revolut.Me
        order.payment_status = "PAYMENT_SUBMITTED"
        order.save(update_fields=["payment_status"])
        return redirect("checkout_confirm")

    return render(
        request,
        "checkout/payment.html",
        {"order": order, "cart_total_cost": cart_total_cost},
    )


def confirm(request):
    """
    Order summary page after user clicks "I have paid".
    """
    order_id = request.session.get("checkout_order_id")
    if not order_id:
        return redirect("checkout_address")

    order = get_object_or_404(Order, id=order_id)
    return render(request, "checkout/confirm.html", {"order": order})


def checkout_success(request):
    """
    Success page (you can mark PAID manually from admin).
    Clears session cart/shipping/order_id.
    """
    request.session["cart"] = {}
    request.session["shipping"] = None
    request.session["checkout_order_id"] = None
    request.session.modified = True
    return render(request, "checkout/success.html")


def checkout_cancel(request):
    """
    Cancel page (keep cart/order so user can try again).
    """
    return render(request, "checkout/cancel.html")


def success(request):
    # Keep compatibility if urls call 'success'
    return checkout_success(request)
