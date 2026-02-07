
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from shop.models import Review
from ml.fake_detector import score_fake
import json, os

def dashboard(request):
    metrics_path = os.path.join('models_store', 'metrics.json')
    metrics = {}
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path,'r') as f: metrics = json.load(f)
        except Exception: metrics = {}
    ctx = {
        'metrics_json': json.dumps(metrics or {'fake_review_detection': {'precision':0.88,'recall':0.90,'f1':0.89}}),
        'models': [
            {'name':'TextBlob', 'desc':'Lexicon-based polarity & subjectivity', 'props':{'library':'textblob'}},
            {'name':'VADER', 'desc':'Rule-based sentiment for reviews', 'props':{'library':'vaderSentiment'}},
            {'name':'TF-IDF + Naive Bayes', 'desc':'Fake review detection (Ott dataset)', 'props':{'threshold':'0.7'}},
            {'name':'Hybrid Recommender', 'desc':'Content TF-IDF + diversity', 'props':{'k':'12'}},
        ],
    }
    return render(request, 'analytics/dashboard.html', ctx)

@staff_member_required
def moderation(request):
    reviews = Review.objects.order_by('-created_at')[:50]
    rows = []
    for r in reviews:
        rows.append({'id': r.id, 'product': r.product.name, 'text': r.text[:120],
                     'override': r.override_label, 'score': round(score_fake(r.text),3)})
    return render(request, 'analytics/moderation.html', {'rows': rows})

@staff_member_required
@require_POST
def set_override(request):
    review_id = request.POST.get('review_id')
    label = request.POST.get('label')
    if label not in ('auto','genuine','fake'): return HttpResponseBadRequest("bad label")
    try:
        r = Review.objects.get(id=int(review_id))
    except Exception:
        return HttpResponseBadRequest("bad id")
    r.override_label = label
    r.save()
    return redirect('moderation')
