from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import vstack
from shop.models import Product
from django.db.models import Avg

_VEC = None
_X = None
_IDS = None

def _ensure_index():
    """Build or reuse a TF-IDF index of product name+description for content recs."""
    global _VEC, _X, _IDS
    if _VEC is not None:
        return

    qs = Product.objects.all().values('id', 'description', 'name')
    texts, ids = [], []
    for r in qs:
        ids.append(r['id'])
        texts.append((r['name'] or '') + ' ' + (r['description'] or ''))

    # If no catalog (first boot), create an empty index and return safely
    if not texts:
        _VEC = TfidfVectorizer()
        _X = None
        _IDS = []
        return

    _VEC = TfidfVectorizer(max_features=10000, ngram_range=(1, 2), min_df=2)
    _X = _VEC.fit_transform(texts)
    _IDS = ids

def recommend_similar_items(product_id: int, k: int = 8):
    _ensure_index()
    if not _IDS or _X is None:
        return Product.objects.none()
    if product_id not in _IDS:
        return Product.objects.order_by('?')[:k]

    idx = _IDS.index(product_id)
    sims = cosine_similarity(_X[idx], _X).ravel()
    order = sims.argsort()[::-1]
    rec_ids = [_IDS[i] for i in order if _IDS[i] != product_id][:k]
    mapping = {p.id: p for p in Product.objects.filter(id__in=rec_ids)}
    return [mapping[i] for i in rec_ids]

def recommend_for_user(user_id: int, k: int = 12):
    _ensure_index()
    # Start with top-rated as seeds
    top = list(Product.objects.annotate(avg=Avg('reviews__rating')).order_by('-avg')[:60])
    if not _IDS or _X is None:
        return top[:k]

    chosen, vecs = [], []
    for p in top:
        if len(chosen) >= k:
            break
        if p.id not in _IDS:
            chosen.append(p)
            continue
        idx = _IDS.index(p.id)
        vec = _X[idx]
        if not vecs:
            chosen.append(p)
            vecs.append(vec)
            continue
        sims = cosine_similarity(vec, vstack(vecs)).ravel()
        if sims.max() < 0.85:  # diversity threshold
            chosen.append(p)
            vecs.append(vec)
    return chosen[:k]
