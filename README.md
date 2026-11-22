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
- MobileNetV2 CNN and YOLOv8 plant disease predictions
- Per-model prediction confidence and recorded test accuracy
- Light and dark themes
- Responsive farmer dashboard
- Low-confidence disease warnings

## Technology Stack

- Frontend: React, TypeScript, Vite
- Backend: FastAPI, Pydantic, Uvicorn
- Database: SQLite
- Crop ML: Python, scikit-learn, Random Forest
- Disease ML: TensorFlow/Keras MobileNetV2 CNN and Ultralytics YOLOv8
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

The project requires Python 3.12 and Node.js. The first backend setup installs TensorFlow and PyTorch CPU packages and may take several minutes.

### Backend

```powershell
cd backend
py -3.12 -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:SECRET_KEY = "local-development-only-change-this"
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API documentation: http://127.0.0.1:8000/docs

Keep the backend terminal open while using the app. The database is created at `backend/agrismart.db` by default.

### Frontend

```powershell
cd frontend
npm install
npm run dev -- --host 127.0.0.1
```

Application: http://127.0.0.1:5173

## Deploy on Render

The root `render.yaml` defines a static frontend and a Docker-based FastAPI service. The API uses a persistent disk for SQLite and uploaded images. The backend is configured on Render's Standard plan because both TensorFlow and PyTorch load for disease predictions; the frontend is a static site. Review Render's current service and disk pricing before creating the services.

1. Create a new GitHub repository named `AgriSmart-AI` (do not initialize it with a README or license). Sign in to GitHub CLI with `gh auth login` if you will push from the terminal.
2. From this project directory, create and push the project branch:

   ```powershell
   git add -A
   git commit -m "Prepare AgriSmart AI for deployment"
   git remote add agrismart https://github.com/<YOUR_GITHUB_USERNAME>/AgriSmart-AI.git
   git push -u agrismart main
   ```

   If `git add` or `git commit` reports there is nothing to commit, skip that command. Keep the existing `origin` remote unchanged unless you intentionally want to replace it.

3. In the Render Dashboard, choose **New → Blueprint**, connect the new GitHub repository, and select the `render.yaml` at the repository root.
4. Review the two services before applying the Blueprint. It creates:
   - `agrismart-api`: the backend container, a 1 GB persistent disk at `/var/data`, generated `SECRET_KEY`, and production CORS configuration.
   - `agrismart-web`: the static Vite frontend configured to call `https://agrismart-api.onrender.com`.
5. Apply the Blueprint and wait for both services to finish their first deployment. The backend image is large because it contains TensorFlow, PyTorch, and the disease models; the first build and first inference may take several minutes.
6. Confirm the API responds at `https://agrismart-api.onrender.com/api/health` with `{"status":"ok","database":"sqlite"}`. Open `https://agrismart-api.onrender.com/docs` to inspect the API, then open `https://agrismart-web.onrender.com` to use the app.
7. If you change either Render service name or add a custom frontend domain, update `CORS_ORIGINS` on `agrismart-api` to the exact frontend origin (scheme and hostname, no path), then redeploy the backend.

The Render disk preserves the SQLite database and uploaded images across deploys. Back up the disk/database regularly; a single instance and local SQLite file are intended for a small deployment, not horizontally scaled production traffic. Never put `.env` or production secrets in GitHub.

## Crop Model

The crop model uses nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall. It was trained with a stratified 80/20 split and evaluated with five-fold cross-validation.

## Disease Model

The integrated `plant_disease_model.keras` CNN and `AgriSmart_AI_YOLOv8.pt` YOLOv8 classifier support the same 38 PlantVillage classes. The provided corrected CNN test evaluation reports:

- Test images: 8,131
- Test accuracy: 96.5564%
- Macro precision, recall, and F1: approximately 96%

The disease screen runs both this CNN and the YOLOv8 classifier on each image. It labels per-image confidence separately from held-out test accuracy. The MobileNetV2 test accuracy is 96.56%; no YOLOv8 test-accuracy metric was supplied, so the app reports it as unavailable instead of treating confidence as accuracy. Disease predictions should be treated as decision support and are not agricultural guarantees.

## Optional Custom CNN Training

The reference PyTorch CNN can be trained separately when the full 39-class PlantVillage folder dataset is available. See [custom CNN training instructions](docs/custom_cnn_training.md). This produces a `.pt` state-dict checkpoint and does not replace the active Keras MobileNetV2 model automatically.

## Reference Repositories

This project was developed by redesigning and integrating components from the cloned SmartCrop and Plant Disease Detection reference repositories. Their original licenses and author attributions remain applicable.

## Author

Prince Shukla
