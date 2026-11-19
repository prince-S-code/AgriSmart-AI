# AgriSmart AI

**Author and Maintainer: Prince Shukla**

AgriSmart AI is a local agricultural decision-support platform that combines crop recommendation and 38-class plant disease detection in one responsive full-stack application.

## Implemented Features

- React, TypeScript, and Vite frontend
- FastAPI backend
- SQLite database
- Farmer registration and login
- JWT authentication
- User-specific crop and disease history
- Random Forest crop recommendation
- MobileNetV2 plant disease prediction
- Light and dark themes
- Responsive farmer dashboard
- Low-confidence disease warnings

## Technology Stack

- Frontend: React, TypeScript, Vite
- Backend: FastAPI, Pydantic, Uvicorn
- Database: SQLite
- Crop ML: Python, scikit-learn, Random Forest
- Disease ML: TensorFlow, MobileNetV2, Keras
- Authentication: JWT and bcrypt

## Project Structure

```text
AgriSmart-AI/
├── frontend/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── database/
│   │   ├── schemas/
│   │   └── services/
│   ├── scripts/
│   ├── trained_models/
│   └── tests/
└── docs/
```

## Run Locally

### Backend

```powershell
cd backend
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API documentation: http://127.0.0.1:8000/docs

### Frontend

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Application: http://127.0.0.1:5173

## Crop Model

The crop model uses nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall. It was trained with a stratified 80/20 split and evaluated with five-fold cross-validation.

## Disease Model

The integrated `AgriSmart_AI_MobileNetV2.keras` model supports 38 PlantVillage classes. The provided corrected test evaluation reports:

- Test images: 8,131
- Test accuracy: 96.5564%
- Macro precision, recall, and F1: approximately 96%

Disease predictions should be treated as decision support and are not medical or agricultural guarantees.

## Optional Custom CNN Training

The reference PyTorch CNN can be trained separately when the full 39-class PlantVillage folder dataset is available. See [custom CNN training instructions](docs/custom_cnn_training.md). This produces a `.pt` state-dict checkpoint and does not replace the active Keras MobileNetV2 model automatically.

## Reference Repositories

This project was developed by redesigning and integrating components from the cloned SmartCrop and Plant Disease Detection reference repositories. Their original licenses and author attributions remain applicable.

## Author

Prince Shukla
