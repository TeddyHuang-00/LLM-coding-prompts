"""Transformer model implementation"""

from __future__ import annotations

import torch
from torch import nn
from torch.nn import TransformerEncoder, TransformerEncoderLayer

from .base import BaseModel


class TransformerModel(BaseModel):
    """Simple Transformer model for sequence classification"""

    def _build_model(self, **kwargs: dict) -> nn.Module:
        """Build Transformer architecture"""
        # Extract configuration
        input_size = kwargs.get("input_size", 512)
        num_classes = kwargs.get("num_classes", 10)
        hidden_size = kwargs.get("hidden_size", 256)
        num_layers = kwargs.get("num_layers", 6)
        num_heads = kwargs.get("num_heads", 8)
        dropout = kwargs.get("dropout", 0.1)

        return TransformerClassifier(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            num_heads=num_heads,
            num_classes=num_classes,
            dropout=dropout,
        )


class TransformerClassifier(nn.Module):
    """Transformer-based classifier"""

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_layers: int,
        num_heads: int,
        num_classes: int,
        dropout: float = 0.1,
    ) -> None:
        super().__init__()

        # Input projection
        self.input_projection = nn.Linear(input_size, hidden_size)

        # Positional encoding
        self.pos_encoder = PositionalEncoding(hidden_size, dropout)

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
            nn.Linear(hidden_size, num_classes),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Forward pass"""
        # x shape: (batch_size, seq_len, input_size)
        x = self.input_projection(x)
        x = self.pos_encoder(x)

        # Transformer encoding
        x = self.transformer_encoder(x)

        # Global average pooling over sequence dimension
        x = torch.mean(x, dim=1)

        # Classification
        return self.classifier(x)


class PositionalEncoding(nn.Module):
    """Positional encoding for transformer"""

    def __init__(self, d_model: int, dropout: float = 0.1, max_len: int = 5000) -> None:
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float()
            * (-torch.log(torch.tensor(10000.0)) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer("pe", pe)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Add positional encoding to input"""
        x = x + self.pe[:, : x.size(1), :]
        return self.dropout(x)
