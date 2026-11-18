# Repository Analysis

## Plant disease repository

- Stack: Flask, PyTorch/Torchvision, PIL, NumPy, Pandas.
- Architecture: a custom 39-class `torch.nn.Module` loaded from a state-dictionary file.
- Training: the notebook uses PlantVillage-style `ImageFolder`, 224×224 center-cropped tensors, shuffled 85/15 holdout and 70/30 train/validation split inside the training portion.
- Available reusable components: crop/disease knowledge CSV structure, image preprocessing concept, CNN architecture, 39-class mapping.
- Missing/weak: no model artifact is present in the workspace; no MobileNetV2 implementation; no independent test-set methodology proven; no robust JPEG/PNG validation, confidence extraction, or user isolation; Flask debug mode; filename-based upload storage; known dependencies are outdated and the README expects users to supply a model manually.
- Security: unrestricted filenames, shared upload directory, no authentication, no authorization, and debug server mode.

## Crop repository

- Stack: Streamlit, pandas, scikit-learn, pickle, Plotly/Seaborn.
- Dataset: `SmartCrop-Dataset.csv`, 7 features plus `label`, with nitrogen, phosphorus, potassium, temperature, humidity, pH, rainfall.
- Available reusable components: seven-feature data format and a serialized `model.pkl` artifact.
- Model: the active training code replaces the explored ensemble candidates with `StandardScaler + GaussianNB`; Random Forest/XGBoost comparisons and independent test methodology are not retained in a reproducible pipeline.
- Weaknesses: old pinned dependencies, pandas-profiling deprecation risk, fixed input limits too loose and too narrow for some real units, no top-three support, no probability calibration, no model metadata, no authentication or history.
- License: the repository has an MIT license. Preserve attribution and license notices.

## Comparative decision

MongoDB is selected for primary storage because user history and knowledge data are document-shaped, predictions are append-heavy and queried independently from users, and PostgreSQL would add more joins and migration overhead without a demonstrated requirement for relational transactions. PostgreSQL remains an optional future alternative only if relational reporting needs emerge.

## Proposed unified architecture

- React/Vite/TypeScript frontend.
- FastAPI backend with modular auth, profile, ML, history, knowledge, dashboard, and reporting routes.
- MongoDB Atlas/local MongoDB with JSON schema validation and indexed history queries.
- Real backend ML inference only; no demo values in production endpoints.
- A real disease model is required before disease inference can be enabled.
- The existing crop artifact can be reused only after runtime inspection and retraining/replacing with a versioned pipeline that has reproducible metrics.
