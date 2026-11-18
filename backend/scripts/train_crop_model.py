import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

BASE = Path(__file__).resolve().parents[1]
DATA = Path(__file__).resolve().parents[3] / "SmartCrop-master" / "SmartCrop-Dataset.csv"
MODEL_DIR = BASE / "trained_models" / "crop"


def main():
    df = pd.read_csv(DATA)
    X = df[["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]]
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )
    model = RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        min_samples_leaf=1,
        class_weight="balanced",
        random_state=42,
        n_jobs=-1,
    )
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy")

    model.fit(X_train, y_train)
    predictions = model.predict(X_test)
    test_accuracy = accuracy_score(y_test, predictions)

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with (MODEL_DIR / "crop_model.pkl").open("wb") as file:
        pickle.dump(model, file)

    metadata = {
        "model_name": "RandomForestClassifier",
        "features": X.columns.tolist(),
        "classes": sorted(y.unique().tolist()),
        "training_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "cv_accuracy_mean": float(cv_scores.mean()),
        "cv_accuracy_std": float(cv_scores.std()),
        "test_accuracy": float(test_accuracy),
        "random_seed": 42,
    }
    (MODEL_DIR / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(json.dumps(metadata, indent=2))
    print(classification_report(y_test, predictions))


if __name__ == "__main__":
    main()
