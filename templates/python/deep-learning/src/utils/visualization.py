"""Visualization utilities for training and evaluation"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import torch


def plot_training_history(
    train_losses: list[float],
    val_losses: list[float],
    train_accs: list[float] | None = None,
    val_accs: list[float] | None = None,
    save_path: Path | None = None,
) -> None:
    """Plot training history"""
    epochs = range(1, len(train_losses) + 1)

    if train_accs is not None and val_accs is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

        # Plot losses
        ax1.plot(epochs, train_losses, label="Train Loss", marker="o")
        ax1.plot(epochs, val_losses, label="Val Loss", marker="s")
        ax1.set_title("Training and Validation Loss")
        ax1.set_xlabel("Epoch")
        ax1.set_ylabel("Loss")
        ax1.legend()
        ax1.grid(True)

        # Plot accuracies
        ax2.plot(epochs, train_accs, label="Train Acc", marker="o")
        ax2.plot(epochs, val_accs, label="Val Acc", marker="s")
        ax2.set_title("Training and Validation Accuracy")
        ax2.set_xlabel("Epoch")
        ax2.set_ylabel("Accuracy")
        ax2.legend()
        ax2.grid(True)
    else:
        fig, ax1 = plt.subplots(1, 1, figsize=(8, 4))
        ax1.plot(epochs, train_losses, label="Train Loss", marker="o")
        ax1.plot(epochs, val_losses, label="Val Loss", marker="s")
        ax1.set_title("Training and Validation Loss")
        ax1.set_xlabel("Epoch")
        ax1.set_ylabel("Loss")
        ax1.legend()
        ax1.grid(True)

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()


def plot_confusion_matrix(
    cm: np.ndarray,
    class_names: list[str] | None = None,
    normalize: bool = False,
    save_path: Path | None = None,
) -> None:
    """Plot confusion matrix"""
    if normalize:
        cm = cm.astype("float") / cm.sum(axis=1)[:, np.newaxis]
        title = "Normalized Confusion Matrix"
        fmt = ".2f"
    else:
        title = "Confusion Matrix"
        fmt = "d"

    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm,
        annot=True,
        fmt=fmt,
        cmap="Blues",
        xticklabels=class_names,
        yticklabels=class_names,
    )
    plt.title(title)
    plt.xlabel("Predicted Label")
    plt.ylabel("True Label")

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()


def visualize_batch(
    images: torch.Tensor,
    labels: torch.Tensor,
    predictions: torch.Tensor | None = None,
    class_names: list[str] | None = None,
    num_samples: int = 8,
    save_path: Path | None = None,
) -> None:
    """Visualize a batch of images with labels and predictions"""
    batch_size = min(num_samples, images.size(0))

    fig, axes = plt.subplots(2, 4, figsize=(12, 6))
    axes = axes.flatten()

    for i in range(batch_size):
        img = images[i].cpu().numpy()

        # Handle different image formats
        if img.ndim == 3:
            if img.shape[0] == 3:  # RGB
                img = np.transpose(img, (1, 2, 0))
            elif img.shape[0] == 1:  # Grayscale
                img = img.squeeze(0)

        # Normalize for display
        img = (img - img.min()) / (img.max() - img.min())

        axes[i].imshow(img, cmap="gray" if img.ndim == 2 else None)

        # Create title
        true_label = labels[i].item()
        title = f"True: {class_names[true_label] if class_names else true_label}"

        if predictions is not None:
            pred_label = torch.argmax(predictions[i]).item()
            pred_name = class_names[pred_label] if class_names else pred_label
            title += f"\nPred: {pred_name}"

            # Color code correct/incorrect predictions
            color = "green" if pred_label == true_label else "red"
            axes[i].set_title(title, color=color)
        else:
            axes[i].set_title(title)

        axes[i].axis("off")

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
    else:
        plt.show()
