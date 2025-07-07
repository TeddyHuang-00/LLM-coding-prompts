"""CNN model implementation"""

from __future__ import annotations

from torch import nn

from .base import BaseModel


class CNNModel(BaseModel):
    """Simple CNN model for image classification"""

    def _build_model(self, **kwargs: dict) -> nn.Module:
        """Build CNN architecture"""
        # Extract configuration
        in_channels = kwargs.get("in_channels", 3)
        num_classes = kwargs.get("num_classes", 10)
        hidden_size = kwargs.get("hidden_size", 64)

        return nn.Sequential(
            # First convolutional block
            nn.Conv2d(in_channels, hidden_size, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_size),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            # Second convolutional block
            nn.Conv2d(hidden_size, hidden_size * 2, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_size * 2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            # Third convolutional block
            nn.Conv2d(hidden_size * 2, hidden_size * 4, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_size * 4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            # Global average pooling
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            # Classifier
            nn.Linear(hidden_size * 4, hidden_size),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(hidden_size, num_classes),
        )
