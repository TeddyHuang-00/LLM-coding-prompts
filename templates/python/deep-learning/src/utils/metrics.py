"""Metrics utilities for model evaluation"""

from __future__ import annotations

import numpy as np
import torch
from sklearn.metrics import classification_report, confusion_matrix


def compute_accuracy(predictions: torch.Tensor, targets: torch.Tensor) -> float:
    """Compute accuracy from predictions and targets"""
    pred_labels = torch.argmax(predictions, dim=1)
    correct = (pred_labels == targets).float()
    return torch.mean(correct).item()


def compute_classification_report(
    predictions: torch.Tensor,
    targets: torch.Tensor,
    class_names: list[str] | None = None,
) -> str:
    """Compute classification report"""
    pred_labels = torch.argmax(predictions, dim=1)

    # Convert to numpy for sklearn
    y_true = targets.cpu().numpy()
    y_pred = pred_labels.cpu().numpy()

    return classification_report(y_true, y_pred, target_names=class_names)


def compute_confusion_matrix(
    predictions: torch.Tensor, targets: torch.Tensor
) -> np.ndarray:
    """Compute confusion matrix"""
    pred_labels = torch.argmax(predictions, dim=1)

    # Convert to numpy for sklearn
    y_true = targets.cpu().numpy()
    y_pred = pred_labels.cpu().numpy()

    return confusion_matrix(y_true, y_pred)


def compute_top_k_accuracy(
    predictions: torch.Tensor, targets: torch.Tensor, k: int = 5
) -> float:
    """Compute top-k accuracy"""
    _, top_k_preds = torch.topk(predictions, k, dim=1)
    targets_expanded = targets.unsqueeze(1).expand_as(top_k_preds)
    correct = torch.any(top_k_preds == targets_expanded, dim=1)
    return torch.mean(correct.float()).item()
