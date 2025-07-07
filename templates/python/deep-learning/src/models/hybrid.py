"""Hybrid CNN-Transformer model implementation"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .base import BaseModel


class HybridModel(BaseModel):
    """Hybrid CNN-Transformer model"""

    def _build_model(self, **kwargs: dict) -> nn.Module:
        """Build hybrid architecture"""
        # Extract configuration
        in_channels = kwargs.get("in_channels", 3)
        num_classes = kwargs.get("num_classes", 10)
        hidden_size = kwargs.get("hidden_size", 256)
        num_layers = kwargs.get("num_layers", 4)
        num_heads = kwargs.get("num_heads", 8)
        dropout = kwargs.get("dropout", 0.1)

        return HybridCNNTransformer(
            in_channels=in_channels,
            hidden_size=hidden_size,
            num_layers=num_layers,
            num_heads=num_heads,
            num_classes=num_classes,
            dropout=dropout,
        )


class HybridCNNTransformer(nn.Module):
    """Hybrid CNN-Transformer architecture"""

    def __init__(
        self,
        in_channels: int,
        hidden_size: int,
        num_layers: int,
        num_heads: int,
        num_classes: int,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()

        # CNN feature extractor
        self.cnn_features = nn.Sequential(
            # First block
            nn.Conv2d(in_channels, hidden_size // 4, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_size // 4),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            # Second block
            nn.Conv2d(hidden_size // 4, hidden_size // 2, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_size // 2),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
            # Third block
            nn.Conv2d(hidden_size // 2, hidden_size, kernel_size=3, padding=1),
            nn.BatchNorm2d(hidden_size),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2),
        )

        # Transformer encoder
        encoder_layer = TransformerEncoderLayer(
            d_model=hidden_size,
            nhead=num_heads,
            dim_feedforward=hidden_size * 4,
            dropout=dropout,
            batch_first=True,
        )
        self.transformer_encoder = TransformerEncoder(encoder_layer, num_layers)

        # Classification head
        self.classifier = nn.Sequential(
            nn.LayerNorm(hidden_size),
            nn.Dropout(dropout),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(inplace=True),
            nn.Dropout(dropout),
            nn.Linear(hidden_size // 2, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass"""
        # CNN feature extraction
        # x shape: (batch_size, channels, height, width)
        features = self.cnn_features(x)

        # Flatten spatial dimensions to create sequence
        # features shape: (batch_size, hidden_size, h', w')
        batch_size, hidden_size, h, w = features.shape
        features = features.view(batch_size, hidden_size, -1).transpose(1, 2)
        # features shape: (batch_size, h'*w', hidden_size)

        # Transformer encoding
        features = self.transformer_encoder(features)

        # Global average pooling over sequence dimension
        features = torch.mean(features, dim=1)

        # Classification
        return self.classifier(features)
