
import os, joblib
from .utils import clean_text
MODEL_PATH = os.getenv("FAKE_MODEL_PATH", "models_store/fake_review_nb.pkl")
VEC_PATH = os.getenv("FAKE_VEC_PATH", "models_store/tfidf.pkl")
_THRESHOLD = float(os.getenv("FAKE_THRESHOLD", "0.7"))
_clf=None; _vec=None
def _load():
    global _clf,_vec
    if _clf is not None and _vec is not None: return
    if os.path.exists(MODEL_PATH) and os.path.exists(VEC_PATH):
        _clf = joblib.load(MODEL_PATH); _vec = joblib.load(VEC_PATH)
    else: _clf,_vec=None,None
def score_fake(text:str)->float:
    _load()
    if not text or _clf is None or _vec is None: return 0.0
    X = _vec.transform([clean_text(text)])
    if hasattr(_clf,"predict_proba"): return float(_clf.predict_proba(X)[0][1])
    return float(_clf.predict(X)[0])
def is_fake(text:str, threshold:float=None)->bool:
    th = threshold if threshold is not None else _THRESHOLD
    return score_fake(text) >= th
