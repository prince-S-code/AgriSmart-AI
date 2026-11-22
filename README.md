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
- Disease ML: TensorFlow Lite MobileNetV2 CNN; optional Ultralytics YOLOv8 on larger instances
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

The project requires Python 3.12 and Node.js. Disease prediction uses the smaller TensorFlow Lite runtime. For training or converting the original Keras disease model, also install `backend/requirements-training.txt`. Install the optional YOLO dependencies only if you have enough memory for both models.

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

The root `render.yaml` defines a static frontend and a Docker-based FastAPI service on Render's Free plan. It uses TensorFlow Lite for CNN inference and disables YOLO to stay within the API instance's memory limit. Free instances have ephemeral storage, so account and history data in SQLite may be lost when the service restarts or redeploys. The disease-upload endpoint deletes each image after inference.

1. Connect the existing `https://github.com/prince-S-code/AgriSmart-AI` repository to Render. Sign in to GitHub CLI with `gh auth login` only if you need to push additional changes from the terminal.
2. Push changes to the existing repository's `main` branch:

   ```powershell
   git add -A
   git commit -m "Prepare AgriSmart AI for deployment"
   git remote add agrismart https://github.com/prince-S-code/AgriSmart-AI.git
   git push -u agrismart main
   ```

   If `git add` or `git commit` reports there is nothing to commit, skip that command. Keep the existing `origin` remote unchanged unless you intentionally want to replace it.

3. In the Render Dashboard, choose **New → Blueprint**, connect the new GitHub repository, and select the `render.yaml` at the repository root.
4. Review the two services before applying the Blueprint. It creates:
   - `agrismart-api`: the backend container, generated `SECRET_KEY`, Free-plan temporary SQLite storage, and production CORS configuration.
   - `agrismart-web`: the static Vite frontend configured to call the backend URL.
5. Apply the Blueprint and wait for both services to finish their first deployment. The backend uses TensorFlow Lite for CNN inference; YOLO is disabled on Free to stay within the memory limit.
6. For the current Render services, confirm the API responds at `https://agrismart-api-tphl.onrender.com/api/health` with `{"status":"ok","database":"sqlite"}`. Open `https://agrismart-api-tphl.onrender.com/docs` to inspect the API, then open `https://agrismart-web-bkln.onrender.com` to use the app. Render can assign different hostnames when creating new services; always use the service URLs shown in its dashboard.
7. If you change either Render service name or add a custom frontend domain, update `CORS_ORIGINS` on the API service to the exact frontend origin (scheme and hostname, no path), then redeploy the backend.

For local YOLO development, install `backend/requirements-yolo.txt` and set `ENABLE_YOLO=true`. To include YOLO in a Docker image, build with `--build-arg INSTALL_YOLO=true` and set `ENABLE_YOLO=true` in the runtime environment. Both models together require more memory than the Render Free instance provides. Never put `.env` or production secrets in GitHub.

## Crop Model

The crop model uses nitrogen, phosphorus, potassium, temperature, humidity, pH, and rainfall. It was trained with a stratified 80/20 split and evaluated with five-fold cross-validation.

## Disease Model

The `plant_disease_model.tflite` CNN and optional `AgriSmart_AI_YOLOv8.pt` YOLOv8 classifier support the same 38 PlantVillage classes. The original Keras CNN was exported to float32 TFLite and its outputs were checked for parity. The provided corrected CNN test evaluation reports:

- Test images: 8,131
- Test accuracy: 96.5564%
- Macro precision, recall, and F1: approximately 96%

The disease screen uses the CNN model on Render Free and labels per-image confidence separately from held-out test accuracy. The original MobileNetV2 model's recorded test accuracy is 96.56%; the TFLite export retains its float32 weights. No YOLOv8 test-accuracy metric was supplied, so the app reports it as unavailable instead of treating confidence as accuracy. Disease predictions should be treated as decision support and are not agricultural guarantees.

## Optional Custom CNN Training

The reference PyTorch CNN can be trained separately when the full 39-class PlantVillage folder dataset is available. See [custom CNN training instructions](docs/custom_cnn_training.md). This produces a `.pt` state-dict checkpoint and does not replace the active MobileNetV2 CNN automatically.

## Reference Repositories

This project was developed by redesigning and integrating components from the cloned SmartCrop and Plant Disease Detection reference repositories. Their original licenses and author attributions remain applicable.

## Author

Prince Shukla
