# Training the Reference Custom CNN

**Author and Maintainer: Prince Shukla**

This workflow trains the PyTorch architecture in `Plant-Disease-Detection-main/Flask Deployed App/CNN.py`. It expects a PlantVillage-style folder dataset with exactly the 39 class folders named by `CNN.idx_to_classes`.

## Dataset Layout

Place the complete dataset at:

```text
Plant-Disease-Detection-main/Model/Dataset/
├── Apple___Apple_scab/
├── Apple___Black_rot/
├── ...
└── Tomato___healthy/
```

The folder names must exactly match all 39 names in `CNN.idx_to_classes`. The dataset is not currently present in this workspace. The 40 images in `test_images/` are individual examples and are not enough to train or evaluate a 39-class model.

## Environment

From the AgriSmart project root in PowerShell:

```powershell
py -3.12 -m venv .venv-custom-cnn
.\.venv-custom-cnn\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r backend/scripts/requirements-custom-cnn.txt
```

For CUDA training, install the PyTorch build matching the installed NVIDIA driver/CUDA using the official PyTorch installation selector, then install the remaining packages in the requirements file.

## Train

```powershell
python backend/scripts/train_custom_cnn.py --epochs 30 --batch-size 4
```

If the dataset is in another location:

```powershell
python backend/scripts/train_custom_cnn.py --dataset "D:\datasets\PlantVillage" --epochs 30 --batch-size 4
```

The trainer makes a deterministic stratified 70/15/15 train/validation/test split, applies light augmentation to training images, selects the checkpoint using validation accuracy, early-stops, and reports final held-out test accuracy, per-class scores, and a confusion matrix.

The CNN is large (about 52.6 million parameters). Batch size 4 is a conservative starting point. Lower it if memory is insufficient. CPU training can take a long time.

## Output

By default, the script writes:

```text
AgriSmart-AI/backend/trained_models/custom_cnn/
├── plant_disease_model_1_latest.pt
└── metadata.json
```

The `.pt` file is a PyTorch `state_dict`, compatible with `CNN.CNN(39)`. `metadata.json` records its class order and held-out evaluation. The active AgriSmart API currently uses the Keras MobileNetV2 artifact; this custom CNN checkpoint does not replace that model automatically.
