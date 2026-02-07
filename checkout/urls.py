from django.urls import path
from . import views

urlpatterns = [
    path("address/", views.address, name="checkout_address"),
    path("payment/", views.payment, name="checkout_payment"),
    path("confirm/", views.confirm, name="checkout_confirm"),
    path("success/", views.checkout_success, name="checkout_success"),
    path("cancel/", views.checkout_cancel, name="checkout_cancel"),
]
