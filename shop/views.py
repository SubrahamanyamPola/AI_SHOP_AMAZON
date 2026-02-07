
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg, Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Category, Product, Review
from .forms import SearchForm, ReviewForm
from ml.sentiment_engine import sentiment_textblob, sentiment_vader
from ml.simple_hybrid import recommend_for_user, recommend_similar_items
from ml.fake_detector import score_fake

def home(request):
    products = Product.objects.annotate(n_rev=Count('reviews')).order_by('-n_rev')[:12]
    return render(request, 'shop/home.html', {'products': products})

def category_view(request, slug):
    cat = get_object_or_404(Category, slug=slug)
    products = cat.products.all()
    return render(request, 'shop/category.html', {'category': cat, 'products': products})

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == 'POST' and request.user.is_authenticated:
        form = ReviewForm(request.POST)
        if form.is_valid():
            Review.objects.create(product=product, user=request.user,
                                  rating=form.cleaned_data['rating'],
                                  text=form.cleaned_data['text'])
            messages.success(request, "Review added.")
            return redirect('product_detail', slug=slug)
    else:
        form = ReviewForm()
    reviews_qs = product.reviews.order_by('-created_at')[:20]
    tb, vd = [], []
    reviews = []
    for r in reviews_qs:
        tbp = sentiment_textblob(r.text)['polarity']
        vdp = sentiment_vader(r.text)['compound']
        fp = score_fake(r.text)
        use_fake = (r.override_label == 'fake') or (r.override_label == 'auto' and fp >= 0.7)
        tb.append(tbp); vd.append(vdp)
        reviews.append({'rating': r.rating,'text': r.text,'created_at': r.created_at,
                        'tb': round(tbp,3),'vd': round(vdp,3),'fake_score': round(fp,3),
                        'is_fake': use_fake,'override': r.override_label})
    s = {'count': len(reviews), 'tb_avg': round(sum(tb)/len(tb),3) if tb else 0.0,
         'vd_avg': round(sum(vd)/len(vd),3) if vd else 0.0}
    sim_items = recommend_similar_items(product.id, k=8)
    return render(request, 'shop/product_detail.html', {'product': product, 'reviews': reviews,
                                                       'sentiment': s, 'similar_items': sim_items,
                                                       'form': form})

def search(request):
    form = SearchForm(request.GET)
    products = Product.objects.none()
    query = ""
    if form.is_valid():
        query = form.cleaned_data.get('q') or ""
        cat = form.cleaned_data.get('cat')
        qs = Product.objects.all()
        if cat: qs = qs.filter(category__slug=cat)
        if query: qs = qs.filter(Q(name__icontains=query) | Q(description__icontains=query))
        products = qs[:48]
    return render(request, 'shop/search.html', {'products': products, 'query': query})

@login_required
def recommendations(request):
    items = recommend_for_user(request.user.id, k=12)
    return render(request, 'shop/recommendations.html', {'products': items})
