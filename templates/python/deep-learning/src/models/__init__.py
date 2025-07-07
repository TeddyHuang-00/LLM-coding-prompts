"""Model factory and registry"""

from __future__ import annotations

from .base import BaseModel
from .cnn import CNNModel
from .hybrid import HybridModel
from .transformer import TransformerModel

__all__ = ["BaseModel", "CNNModel", "HybridModel", "TransformerModel", "create_model"]


def create_model(model_type: str, **kwargs: dict) -> BaseModel:
    """Create model instance based on type"""
    model_registry = {
        "cnn": CNNModel,
        "transformer": TransformerModel,
        "hybrid": HybridModel,
    }

    if model_type not in model_registry:
        available = ", ".join(model_registry.keys())
        msg = f"Unknown model type: {model_type}. Available: {available}"
        raise ValueError(msg)

    return model_registry[model_type](**kwargs)
