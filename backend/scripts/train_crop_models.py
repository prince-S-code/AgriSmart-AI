from pathlib import Path
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

ROOT = Path(__file__).resolve().parents[1]
DATA = Path(r"C:\Users\princ\Documents\GitHub\Agri AI\SmartCrop-master\SmartCrop-Dataset.csv")
OUT = ROOT / "trained_models" / "crop"
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(DATA)
    X = df[FEATURES]
    y = df["label"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    candidates = {
        "gaussian_nb": Pipeline([("scaler", StandardScaler()), ("model", GaussianNB())]),
        "random_forest": RandomForestClassifier(n_estimators=300, max_depth=None, min_samples_leaf=1, random_state=42, n_jobs=-1),
    }
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    results = {}
    best_name, best_model, best_accuracy = None, None, -1
    for name, model in candidates.items():
        cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy", n_jobs=-1)
        model.fit(X_train, y_train)
        accuracy = accuracy_score(y_test, model.predict(X_test))
        results[name] = {"cv_accuracy_mean": float(cv_scores.mean()), "cv_accuracy_std": float(cv_scores.std()), "test_accuracy": float(accuracy)}
        if accuracy > best_accuracy:
            best_name, best_model, best_accuracy = name, model, accuracy
    joblib.dump(best_model, OUT / "crop_model.joblib")
    (OUT / "crop_metadata.json").write_text(json.dumps({
        "model_name": best_name,
        "dataset": str(DATA),
        "rows": len(df),
        "features": FEATURES,
        "classes": sorted(y.unique()),
        "test_method": "20% stratified holdout plus 5-fold stratified cross-validation",
        "results": results,
    }, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))
    print(f"Saved {best_name} to {OUT / 'crop_model.joblib'}")


if __name__ == "__main__":
    main()
