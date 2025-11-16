import argparse
import json
import os
from pathlib import Path
from typing import Dict, List

import torch
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as T
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder

# Optional: sklearn metrics for detailed report
try:
    from sklearn.metrics import classification_report, confusion_matrix
    HAVE_SKLEARN = True
except Exception:
    HAVE_SKLEARN = False


def build_model(num_classes: int) -> nn.Module:
    model = models.resnet50(weights=None)
    num_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_features, 512),
        nn.ReLU(),
        nn.BatchNorm1d(512),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes),
    )
    return model


def get_transforms() -> T.Compose:
    return T.Compose([
        T.Resize((256, 256)),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
    ])


def load_idx_maps(classes_json: Path):
    with open(classes_json, "r", encoding="utf-8") as f:
        idx_to_name: Dict[str, str] = json.load(f)
    name_to_idx = {v: int(k) for k, v in idx_to_name.items()}
    ordered_names: List[str] = [idx_to_name[str(i)] for i in range(len(idx_to_name))]
    return idx_to_name, name_to_idx, ordered_names


def evaluate(classes_json: Path, weights_path: Path, data_dir: Path, batch_size: int = 32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    if not classes_json.exists():
        raise FileNotFoundError(f"Classes json not found: {classes_json}")
    if not weights_path.exists():
        raise FileNotFoundError(f"Weights file not found: {weights_path}")
    if not data_dir.exists():
        raise FileNotFoundError(f"Data directory not found: {data_dir}")

    idx_to_name, name_to_idx, ordered_names = load_idx_maps(classes_json)

    # Dataset
    transform = get_transforms()
    ds = ImageFolder(str(data_dir), transform=transform)

    if len(ds.classes) == 0:
        raise RuntimeError(f"No classes found in {data_dir}. Expected subfolders per class.")

    # Map ImageFolder class index -> model class index
    folder_to_model = {}
    for folder_name, folder_idx in ds.class_to_idx.items():
        if folder_name not in name_to_idx:
            raise KeyError(
                f"Class folder '{folder_name}' not found in {classes_json}. "
                f"Available: {list(name_to_idx.keys())}"
            )
        folder_to_model[folder_idx] = name_to_idx[folder_name]

    loader = DataLoader(ds, batch_size=batch_size, shuffle=False, num_workers=0)

    # Model
    model = build_model(num_classes=len(ordered_names))
    ckpt = torch.load(str(weights_path), map_location=device)
    state = ckpt.get("model_state_dict", ckpt)
    model.load_state_dict(state)
    model.to(device).eval()

    # Inference
    y_true_all: List[int] = []
    y_pred_all: List[int] = []

    with torch.no_grad():
        for x, y_folder_idx in loader:
            x = x.to(device)
            y_model_idx = torch.tensor([folder_to_model[int(i)] for i in y_folder_idx], device=device)
            logits = model(x)
            preds = torch.argmax(torch.softmax(logits, dim=1), dim=1)
            y_true_all.extend(y_model_idx.cpu().tolist())
            y_pred_all.extend(preds.cpu().tolist())

    # Metrics
    correct = sum(1 for t, p in zip(y_true_all, y_pred_all) if t == p)
    acc = 100.0 * correct / len(y_true_all) if y_true_all else 0.0

    print("\n================ Evaluation Report ================")
    print(f"Data dir      : {data_dir}")
    print(f"Weights       : {weights_path}")
    print(f"Classes JSON  : {classes_json}")
    print(f"Samples       : {len(y_true_all)}")
    print(f"Top-1 Accuracy: {acc:.2f}%")

    if HAVE_SKLEARN:
        labels = list(range(len(ordered_names)))
        print("\nClassification Report:")
        print(classification_report(y_true_all, y_pred_all, labels=labels, target_names=ordered_names, digits=3))
        print("Confusion Matrix:")
        print(confusion_matrix(y_true_all, y_pred_all, labels=labels))
    else:
        print("(Tip) Install scikit-learn for detailed metrics: pip install scikit-learn")

    return acc


def main():
    parser = argparse.ArgumentParser(description="Evaluate image classifier accuracy on a folder of classed images.")
    parser.add_argument("--classes-json", required=True, help="Path to classes json used during training")
    parser.add_argument("--weights", required=True, help="Path to model weights (.pth)")
    parser.add_argument("--data-dir", required=True, help="Root folder containing subfolders per class with images")
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()

    evaluate(Path(args.classes_json), Path(args.weights), Path(args.data_dir), args.batch_size)


if __name__ == "__main__":
    main()
