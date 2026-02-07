# from django.urls import path
# from .views import register
# urlpatterns=[path('register/', register, name='register')]
from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import register

urlpatterns = [
    path('register/', register, name='register'),

    # override logout so GET works
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path('', include('django.contrib.auth.urls')),
]
