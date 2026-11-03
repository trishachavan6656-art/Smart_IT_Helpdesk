# Ticket category classifier

The classifier offers an optional category suggestion on the new-ticket form.
The user still chooses and may change the category before submitting; the
server validates the submitted value against the application's supported
categories.

## Implementation

- **Dataset:** 19 short, hand-written examples embedded in
  [`ml_classifier.py`](../ml_classifier.py), covering all seven ticket
  categories. This is a small illustrative dataset, not a representative
  sample of real helpdesk tickets.
- **Preprocessing:** scikit-learn's default `TfidfVectorizer` lowercases text
  and tokenizes it. Stop-word removal is not configured. No external or
  personal data is used for training.
- **Model:** a scikit-learn `Pipeline` combining TF-IDF and Logistic
  Regression (`max_iter=1000`). The model is trained in process and cached
  for subsequent requests.
- **Prediction:** `POST /api/predict-category` requires authentication and
  CSRF validation. Descriptions shorter than five characters are rejected.
  The result is a suggestion, not a change to the ticket record.
- **Supported labels:** `Hardware`, `Software`, `Network`, `Printer`,
  `Account/Login`, `Security`, and `Other`.

## Evaluation

Run the evaluation against the checked-in sample data:

```powershell
python ml_classifier.py
```

The command uses two-fold stratified cross-validation with a fixed random seed
and prints accuracy, macro-averaged precision/recall/F1, and a confusion
matrix. Each example is predicted by a model that was not trained on that
example. Metrics are reproducible for the current dataset but are not evidence
of production accuracy: the dataset is tiny, hand-written, and not an
independent real-world test set. Re-evaluate on a larger, representative,
appropriately consented and labeled dataset before making operational claims.
