
import os, json
import pandas as pd, joblib
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import precision_recall_fscore_support
from ml.utils import clean_text
DATA_PATH = "data/ott_dataset.csv"
MODEL_PATH = "models_store/fake_review_nb.pkl"
VEC_PATH = "models_store/tfidf.pkl"
METRICS_PATH = "models_store/metrics.json"
os.makedirs("models_store", exist_ok=True)
def main():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("Place Ott dataset at data/ott_dataset.csv with columns review,label")
    df = pd.read_csv(DATA_PATH)
    if not {'review','label'}.issubset(df.columns):
        raise ValueError("CSV must have columns review,label (0 genuine, 1 fake)")
    df['clean'] = df['review'].fillna('').apply(clean_text)
    X_train, X_test, y_train, y_test = train_test_split(df['clean'], df['label'], test_size=0.2, random_state=42, stratify=df['label'])
    vec = TfidfVectorizer(max_features=8000, ngram_range=(1,2), min_df=3)
    Xtr = vec.fit_transform(X_train); Xte = vec.transform(X_test)
    clf = MultinomialNB().fit(Xtr, y_train)
    preds = clf.predict(Xte)
    pr, rc, f1, _ = precision_recall_fscore_support(y_test, preds, average='binary')
    joblib.dump(clf, MODEL_PATH); joblib.dump(vec, VEC_PATH)
    metrics = {'fake_review_detection': {'precision': round(float(pr),3), 'recall': round(float(rc),3), 'f1': round(float(f1),3)}}
    if os.path.exists(METRICS_PATH):
        try: old = json.load(open(METRICS_PATH)); old.update(metrics); metrics = old
        except Exception: pass
    with open(METRICS_PATH,'w') as f: json.dump(metrics, f, indent=2)
    print("Saved:", MODEL_PATH, VEC_PATH, METRICS_PATH)
if __name__ == "__main__": main()
