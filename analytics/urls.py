
from django.urls import path
from .views import dashboard, moderation, set_override
urlpatterns = [
    path('', dashboard, name='analytics_dashboard'),
    path('moderation/', moderation, name='moderation'),
    path('moderation/set/', set_override, name='set_override'),
]
