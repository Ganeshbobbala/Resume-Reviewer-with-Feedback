import os
import sys
import json
import logging
import argparse
from typing import Dict, Any, Tuple
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, precision_recall_fscore_support, confusion_matrix
import joblib

# Ensure backend root on sys.path
backend_dir = os.path.abspath(os.path.dirname(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from services.text_processor import preprocess_text

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("train_classifier")

DEFAULT_DATA_PATH = os.path.join(backend_dir, "data", "resumes_corpus.json")
EVAL_DIR = os.path.join(backend_dir, "evaluation")
os.makedirs(EVAL_DIR, exist_ok=True)

def load_and_validate_dataset(filepath: str) -> Tuple[list, list, list]:
    """Loads corpus, verifies schema, removes duplicates and personal data."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Dataset file not found at {filepath}")

    with open(filepath, "r", encoding="utf-8") as f:
        records = json.load(f)

    logger.info(f"Loaded {len(records)} records from {filepath}")
    seen_texts = set()
    cleaned_texts = []
    labels = []
    metadata = []

    for r in records:
        text = r.get("text", "").strip()
        label = r.get("role_target", r.get("category", "")).strip()
        if not text or not label:
            continue
        # Deduplication check
        norm_key = text[:100].lower()
        if norm_key in seen_texts:
            continue
        seen_texts.add(norm_key)

        cleaned_texts.append(preprocess_text(text))
        labels.append(label)
        metadata.append({"id": r.get("id"), "source": r.get("source", "curated")})

    return cleaned_texts, labels, metadata

def train_and_evaluate(
    data_path: str = DEFAULT_DATA_PATH,
    random_seed: int = 42,
    save_artifacts: bool = False
) -> Dict[str, Any]:
    """
    Trains and evaluates the classifier pipeline with reproducible splits,
    preventing data leakage and reporting honest metrics.
    """
    texts, labels, metadata = load_and_validate_dataset(data_path)
    unique_labels, counts = np.unique(labels, return_counts=True)
    class_dist = dict(zip(unique_labels, [int(c) for c in counts]))
    logger.info(f"Class distribution: {class_dist}")

    # Stratified split: 70% train, 30% held-out test
    # If a class has fewer than 2 samples, we fallback to non-stratified random split
    min_count = min(counts)
    stratify = labels if min_count >= 2 else None

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.30,
        random_state=random_seed,
        stratify=stratify
    )

    vectorizer = TfidfVectorizer(
        ngram_range=(1, 2),
        max_features=2500,
        sublinear_tf=True,
        min_df=1
    )
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    # Model 1: MultinomialNB (Baseline)
    nb_clf = MultinomialNB(alpha=0.5)
    nb_clf.fit(X_train_vec, y_train)
    nb_preds = nb_clf.predict(X_test_vec)

    # Model 2: LinearSVC (Enhanced Baseline)
    svc_clf = LinearSVC(C=1.0, random_state=random_seed)
    svc_clf.fit(X_train_vec, y_train)
    svc_preds = svc_clf.predict(X_test_vec)

    # Metrics computation
    def compute_metrics(y_true, y_pred, model_name):
        acc = float(accuracy_score(y_true, y_pred))
        p_macro, r_macro, f1_macro, _ = precision_recall_fscore_support(
            y_true, y_pred, average="macro", zero_division=0
        )
        p_weighted, r_weighted, f1_weighted, _ = precision_recall_fscore_support(
            y_true, y_pred, average="weighted", zero_division=0
        )
        report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
        cm = confusion_matrix(y_true, y_pred).tolist()
        return {
            "model_name": model_name,
            "accuracy": round(acc, 4),
            "macro_precision": round(float(p_macro), 4),
            "macro_recall": round(float(r_macro), 4),
            "macro_f1": round(float(f1_macro), 4),
            "weighted_f1": round(float(f1_weighted), 4),
            "confusion_matrix": cm,
            "classification_report": report
        }

    nb_metrics = compute_metrics(y_test, nb_preds, "MultinomialNB (Baseline)")
    svc_metrics = compute_metrics(y_test, svc_preds, "LinearSVC (Enhanced)")

    results = {
        "dataset_metadata": {
            "provenance": "Curated benchmark tech resume corpus",
            "total_samples": len(texts),
            "train_samples": len(X_train),
            "test_samples": len(X_test),
            "random_seed": random_seed,
            "class_distribution": class_dist,
            "weak_classes": [k for k, v in class_dist.items() if v < 2]
        },
        "multinomial_nb_baseline": nb_metrics,
        "linearsvc_enhanced": svc_metrics
    }

    # Save metrics report
    metrics_path = os.path.join(EVAL_DIR, "baseline_classifier_metrics.json")
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    logger.info(f"Saved evaluation metrics to {metrics_path}")

    # Optionally save artifacts if requested
    if save_artifacts:
        models_dir = os.path.abspath(os.path.join(backend_dir, "models"))
        os.makedirs(models_dir, exist_ok=True)
        joblib.dump(svc_clf, os.path.join(models_dir, "resume_classifier.pkl"))
        joblib.dump(vectorizer, os.path.join(models_dir, "tfidf_vectorizer.pkl"))
        logger.info(f"Saved refreshed artifacts to {models_dir}")

    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--save-artifacts", action="store_true", help="Save trained model artifacts")
    args = parser.parse_args()

    res = train_and_evaluate(save_artifacts=args.save_artifacts)
    print("\n--- CLASSIFIER EVALUATION RESULTS ---")
    print(f"Total Samples: {res['dataset_metadata']['total_samples']}")
    print(f"MultinomialNB Baseline Accuracy: {res['multinomial_nb_baseline']['accuracy']} | Macro-F1: {res['multinomial_nb_baseline']['macro_f1']}")
    print(f"LinearSVC Enhanced Accuracy: {res['linearsvc_enhanced']['accuracy']} | Macro-F1: {res['linearsvc_enhanced']['macro_f1']}")
    print(f"Weak/Single-sample classes reported honestly: {res['dataset_metadata']['weak_classes']}")
