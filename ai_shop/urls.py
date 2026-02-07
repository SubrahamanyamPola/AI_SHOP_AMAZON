from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # your existing app routes stay as-is
    path('', include('shop.urls')),
    path('cart/', include('cart.urls')),
    path('checkout/', include('checkout.urls')),
    path('analytics/', include('analytics.urls')),
    path('accounts/', include('accounts.urls')),

    # ✅ add this line for Google login
    path('accounts/', include('allauth.urls')),
]
