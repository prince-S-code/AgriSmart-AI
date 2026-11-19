import argparse
import copy
import importlib.util
import json
import random
import sys
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, Dataset, Subset
from torchvision import datasets, transforms

REPO_ROOT = Path(__file__).resolve().parents[3]
REFERENCE_ROOT = REPO_ROOT / "Plant-Disease-Detection-main"
CNN_PATH = REFERENCE_ROOT / "Flask Deployed App" / "CNN.py"
DEFAULT_DATASET = REFERENCE_ROOT / "Model" / "Dataset"
DEFAULT_OUTPUT = REPO_ROOT / "AgriSmart-AI" / "backend" / "trained_models" / "custom_cnn"
SEED = 42


class MappedImageFolder(Dataset):
    def __init__(self, dataset, class_to_index):
        self.dataset = dataset
        self.class_to_index = class_to_index
        self.targets = [class_to_index[dataset.classes[target]] for target in dataset.targets]

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, index):
        image, _ = self.dataset[index]
        return image, self.targets[index]


def load_cnn_module():
    if not CNN_PATH.is_file():
        raise FileNotFoundError(f"Expected custom CNN definition at: {CNN_PATH}")
    spec = importlib.util.spec_from_file_location("agrismart_reference_cnn", CNN_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load CNN definition: {CNN_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def evaluate(model, loader, device):
    model.eval()
    all_predictions = []
    all_targets = []
    with torch.inference_mode():
        for images, targets in loader:
            logits = model(images.to(device, non_blocking=True))
            all_predictions.extend(logits.argmax(dim=1).cpu().tolist())
            all_targets.extend(targets.tolist())
    return np.asarray(all_targets), np.asarray(all_predictions)


def main():
    parser = argparse.ArgumentParser(description="Train the reference PyTorch CNN on a class-folder dataset.")
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET, help="Root folder containing one directory per class.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--epochs", type=int, default=30)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--patience", type=int, default=6)
    parser.add_argument("--workers", type=int, default=0)
    args = parser.parse_args()

    if not args.dataset.is_dir():
        raise SystemExit(
            f"Training dataset not found: {args.dataset}\n"
            "Extract PlantVillage into this directory, or pass --dataset PATH. "
            "Do not use the small test_images folder as training data."
        )

    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Training device: {device}")

    cnn_module = load_cnn_module()
    classes = [cnn_module.idx_to_classes[index] for index in sorted(cnn_module.idx_to_classes)]
    class_to_index = {name: index for index, name in enumerate(classes)}

    eval_transform = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
    ])
    train_transform = transforms.Compose([
        transforms.Resize(255),
        transforms.CenterCrop(224),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=10),
        transforms.ToTensor(),
    ])

    eval_folder = datasets.ImageFolder(args.dataset, transform=eval_transform)
    train_folder = datasets.ImageFolder(args.dataset, transform=train_transform)
    if eval_folder.classes != train_folder.classes:
        raise RuntimeError("Train/evaluation folder class order differs")

    missing = sorted(set(classes) - set(eval_folder.classes))
    extra = sorted(set(eval_folder.classes) - set(classes))
    if missing or extra:
        raise ValueError(
            "Dataset classes must match CNN.idx_to_classes exactly.\n"
            f"Missing folders: {missing}\nUnexpected folders: {extra}"
        )

    mapped_dataset = MappedImageFolder(eval_folder, class_to_index)
    mapped_train_dataset = MappedImageFolder(train_folder, class_to_index)
    labels = np.asarray(mapped_dataset.targets)
    indices = np.arange(len(labels))
    train_indices, holdout_indices = train_test_split(
        indices, test_size=0.30, random_state=SEED, stratify=labels
    )
    val_indices, test_indices = train_test_split(
        holdout_indices,
        test_size=0.50,
        random_state=SEED,
        stratify=labels[holdout_indices],
    )

    train_subset = Subset(mapped_train_dataset, train_indices.tolist())
    val_subset = Subset(mapped_dataset, val_indices.tolist())
    test_subset = Subset(mapped_dataset, test_indices.tolist())
    loader_options = {
        "batch_size": args.batch_size,
        "num_workers": args.workers,
        "pin_memory": device.type == "cuda",
    }
    train_loader = DataLoader(train_subset, shuffle=True, **loader_options)
    val_loader = DataLoader(val_subset, shuffle=False, **loader_options)
    test_loader = DataLoader(test_subset, shuffle=False, **loader_options)

    model = cnn_module.CNN(len(classes)).to(device)
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-4, weight_decay=1e-5)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2)

    args.output_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = args.output_dir / "plant_disease_model_1_latest.pt"
    best_state = None
    best_val_accuracy = -1.0
    best_val_loss = float("inf")
    epochs_without_improvement = 0

    for epoch in range(args.epochs):
        started = time.time()
        model.train()
        running_loss = 0.0
        seen = 0
        for images, targets in train_loader:
            images = images.to(device, non_blocking=True)
            targets = targets.to(device, non_blocking=True)
            optimizer.zero_grad(set_to_none=True)
            logits = model(images)
            loss = criterion(logits, targets)
            loss.backward()
            optimizer.step()
            running_loss += loss.item() * targets.size(0)
            seen += targets.size(0)

        train_loss = running_loss / max(seen, 1)
        model.eval()
        val_targets = []
        val_predictions = []
        val_loss_sum = 0.0
        with torch.inference_mode():
            for images, targets in val_loader:
                images = images.to(device, non_blocking=True)
                targets_device = targets.to(device, non_blocking=True)
                logits = model(images)
                val_loss_sum += criterion(logits, targets_device).item() * targets.size(0)
                val_predictions.extend(logits.argmax(dim=1).cpu().tolist())
                val_targets.extend(targets.tolist())
        val_loss = val_loss_sum / max(len(val_subset), 1)
        val_accuracy = accuracy_score(val_targets, val_predictions)
        scheduler.step(val_loss)
        print(
            f"Epoch {epoch + 1}/{args.epochs} | train_loss={train_loss:.4f} "
            f"val_loss={val_loss:.4f} val_accuracy={val_accuracy:.4f} "
            f"duration={time.time() - started:.1f}s"
        )

        if val_accuracy > best_val_accuracy:
            best_val_accuracy = val_accuracy
            best_val_loss = val_loss
            best_state = copy.deepcopy(model.state_dict())
            torch.save(best_state, checkpoint_path)
            epochs_without_improvement = 0
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= args.patience:
                print("Early stopping: validation accuracy did not improve")
                break

    if best_state is None:
        raise RuntimeError("Training ended without producing a best checkpoint")

    model.load_state_dict(best_state)
    test_targets, test_predictions = evaluate(model, test_loader, device)
    report = classification_report(
        test_targets, test_predictions, labels=list(range(len(classes))),
        target_names=classes, output_dict=True, zero_division=0,
    )
    accuracy = float(accuracy_score(test_targets, test_predictions))
    metadata = {
        "model_name": "Custom CNN from CNN.py",
        "dataset_path": str(args.dataset),
        "class_count": len(classes),
        "class_names": classes,
        "input_shape": [3, 224, 224],
        "preprocessing": "Resize(255), CenterCrop(224), ToTensor; training adds horizontal flip and 10-degree rotation",
        "split": {"train": len(train_subset), "validation": len(val_subset), "test": len(test_subset)},
        "seed": SEED,
        "best_validation_accuracy": best_val_accuracy,
        "best_validation_loss": best_val_loss,
        "test_accuracy": accuracy,
        "test_report": report,
        "confusion_matrix": confusion_matrix(test_targets, test_predictions, labels=list(range(len(classes)))).tolist(),
    }
    (args.output_dir / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    print(f"Independent test accuracy: {accuracy:.4%}")
    print(f"Saved state_dict: {checkpoint_path}")
    print(f"Saved class mapping and metrics: {args.output_dir / 'metadata.json'}")


if __name__ == "__main__":
    main()
