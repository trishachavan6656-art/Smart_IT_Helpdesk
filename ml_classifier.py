"""Small TF-IDF and Logistic Regression classifier for ticket categories.

The in-code examples are illustrative training data, not a representative
production dataset. ``python ml_classifier.py`` reports stratified
cross-validation metrics on those examples.
"""

import json
from collections import Counter

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.model_selection import StratifiedKFold, cross_val_predict
from sklearn.pipeline import Pipeline

TRAINING_DATA = [
    ('laptop will not turn on', 'Hardware'),
    ('computer screen is broken', 'Hardware'),
    ('keyboard and mouse are not working', 'Hardware'),
    ('printer paper is jammed', 'Printer'),
    ('printer is not printing documents', 'Printer'),
    ('wifi connection keeps disconnecting', 'Network'),
    ('internet is very slow', 'Network'),
    ('cannot connect to office network', 'Network'),
    ('application crashes when I open it', 'Software'),
    ('software installation failed', 'Software'),
    ('program shows an unexpected error', 'Software'),
    ('cannot login to my account', 'Account/Login'),
    ('password reset is not working', 'Account/Login'),
    ('my account is locked', 'Account/Login'),
    ('suspicious email and possible phishing attack', 'Security'),
    ('antivirus detected malware', 'Security'),
    ('unauthorized access to my computer', 'Security'),
    ('need help with an office issue', 'Other'),
    ('general IT support request', 'Other'),
]

def _new_classifier():
    return Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('classifier', LogisticRegression(max_iter=1000)),
    ])


def build_classifier():
    texts = [text for text, category in TRAINING_DATA]
    labels = [category for text, category in TRAINING_DATA]
    model = _new_classifier()
    model.fit(texts, labels)
    return model


def evaluate_classifier():
    """Return reproducible two-fold stratified metrics for the sample data."""
    texts = [text for text, _category in TRAINING_DATA]
    labels = [category for _text, category in TRAINING_DATA]
    category_counts = Counter(labels)
    if not category_counts or min(category_counts.values()) < 2:
        raise ValueError(
            "Each category needs at least two examples for two-fold "
            "stratified evaluation."
        )

    categories = sorted(category_counts)
    predictions = cross_val_predict(
        _new_classifier(),
        texts,
        labels,
        cv=StratifiedKFold(n_splits=2, shuffle=True, random_state=42),
    )
    return {
        "examples": len(labels),
        "categories": categories,
        "accuracy": accuracy_score(labels, predictions),
        "precision_macro": precision_score(
            labels, predictions, labels=categories, average="macro",
            zero_division=0,
        ),
        "recall_macro": recall_score(
            labels, predictions, labels=categories, average="macro",
            zero_division=0,
        ),
        "f1_macro": f1_score(
            labels, predictions, labels=categories, average="macro",
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(
            labels, predictions, labels=categories
        ).tolist(),
    }


_classifier = None


def predict_category(description):
    global _classifier
    if not description or not description.strip():
        return 'Other'
    if _classifier is None:
        _classifier = build_classifier()
    return _classifier.predict([description.strip()])[0]


if __name__ == "__main__":
    print(json.dumps(evaluate_classifier(), indent=2))
