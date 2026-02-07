
# AI Commerce PRO (Django + NLP + Recs + Fake-Review Moderation)

## Quickstart
```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py shell < scripts/load_sample_data.py
python manage.py runserver
```

- Register/Login (Bootstrap, clean UI)
- Browse categories (Clothes, Electronics, Books)
- Search with category filter
- Product page: TextBlob & VADER sentiment averages + per-review NLP + fake badge
- Add review (logged-in)
- Similar items (TF-IDF content-based) + "My Recommendations" page
- Cart → Address → Payment (demo) → Success with steppers
- Analytics dashboard with cards + charts (Chart.js)
- Moderation (staff): override auto fake/genuine decisions

## Train fake-review detector (Ott et al.)
1. Put CSV at `data/ott_dataset.csv` (columns: `review`, `label` 0/1)
2. Train:
```bash
python scripts/train_fake_review_model.py
```
Artifacts:
- `models_store/fake_review_nb.pkl`
- `models_store/tfidf.pkl`
- `models_store/metrics.json` (displayed on /analytics)

Env overrides:
```
FAKE_MODEL_PATH=models_store/fake_review_nb.pkl
FAKE_VEC_PATH=models_store/tfidf.pkl
FAKE_THRESHOLD=0.7
```
