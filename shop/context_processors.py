
from .models import Category
def category_list(request):
    try:
        cats = Category.objects.all()
    except Exception:
        cats = []
    return {'nav_categories': cats}
