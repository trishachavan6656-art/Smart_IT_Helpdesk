from ml_classifier import TRAINING_DATA, evaluate_classifier, predict_category
from models import TICKET_CATEGORIES


def test_training_labels_use_supported_ticket_categories():
    assert {category for _text, category in TRAINING_DATA} <= set(TICKET_CATEGORIES)


def test_classifier_suggests_existing_categories():
    assert predict_category("office wifi keeps disconnecting") == "Network"
    assert predict_category("my account is locked") == "Account/Login"
    assert predict_category("") == "Other"


def test_classifier_evaluation_reports_metrics_from_all_examples():
    results = evaluate_classifier()

    assert results["examples"] == len(TRAINING_DATA)
    for metric in ("accuracy", "precision_macro", "recall_macro", "f1_macro"):
        assert 0 <= results[metric] <= 1
    assert sum(map(sum, results["confusion_matrix"])) == len(TRAINING_DATA)
