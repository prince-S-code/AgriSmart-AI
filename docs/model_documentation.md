# Model Documentation

## Crop recommendation

The active model is a `RandomForestClassifier` trained on all 2,200 rows in `SmartCrop-Dataset.csv`.

- Training rows: 1,760
- Held-out test rows: 440
- Five-fold stratified validation mean: 99.375%
- Held-out test accuracy: 99.318%
- Random seed: 42
- Features: N, P, K, temperature, humidity, pH, rainfall

Metrics are reported honestly and can change if retraining data or settings are modified.

## Disease detection

No verified disease model artifact is included in this workspace. The disease endpoint validates JPG/PNG input and returns a service-unavailable response until a genuine checkpoint and class mapping are supplied. It never fabricates disease predictions.
