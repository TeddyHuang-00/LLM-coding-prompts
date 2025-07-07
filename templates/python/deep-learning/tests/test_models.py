"""Tests for model modules"""

from __future__ import annotations

import pytest
import torch

from src.models import CNNModel, HybridModel, TransformerModel, create_model
from src.models.base import BaseModel


class TestModelFactory:
    """Test model factory function"""

    def test_create_cnn_model(self) -> None:
        """Test creating CNN model"""
        model = create_model("cnn", num_classes=10, hidden_size=64)
        assert isinstance(model, CNNModel)
        assert isinstance(model, BaseModel)

    def test_create_transformer_model(self) -> None:
        """Test creating Transformer model"""
        model = create_model("transformer", num_classes=10, hidden_size=256)
        assert isinstance(model, TransformerModel)
        assert isinstance(model, BaseModel)

    def test_create_hybrid_model(self) -> None:
        """Test creating Hybrid model"""
        model = create_model("hybrid", num_classes=10, hidden_size=256)
        assert isinstance(model, HybridModel)
        assert isinstance(model, BaseModel)

    def test_invalid_model_type(self) -> None:
        """Test creating model with invalid type"""
        with pytest.raises(ValueError):
            create_model("invalid_model")


class TestCNNModel:
    """Test CNN model"""

    def test_forward_pass(self) -> None:
        """Test forward pass"""
        model = CNNModel(num_classes=10, hidden_size=64)
        x = torch.randn(2, 3, 32, 32)  # Batch of RGB images
        output = model(x)
        assert output.shape == (2, 10)

    def test_training_step(self) -> None:
        """Test training step"""
        model = CNNModel(num_classes=10, hidden_size=64)
        x = torch.randn(2, 3, 32, 32)
        y = torch.randint(0, 10, (2,))
        loss = model.training_step((x, y), 0)
        assert isinstance(loss, torch.Tensor)
        assert loss.dim() == 0  # Scalar loss


class TestTransformerModel:
    """Test Transformer model"""

    def test_forward_pass(self) -> None:
        """Test forward pass"""
        model = TransformerModel(
            input_size=256,
            hidden_size=128,
            num_classes=10,
            num_layers=2,
            num_heads=4,
        )
        x = torch.randn(2, 10, 256)  # Batch of sequences
        output = model(x)
        assert output.shape == (2, 10)

    def test_training_step(self) -> None:
        """Test training step"""
        model = TransformerModel(
            input_size=256,
            hidden_size=128,
            num_classes=10,
            num_layers=2,
            num_heads=4,
        )
        x = torch.randn(2, 10, 256)
        y = torch.randint(0, 10, (2,))
        loss = model.training_step((x, y), 0)
        assert isinstance(loss, torch.Tensor)
        assert loss.dim() == 0  # Scalar loss


class TestHybridModel:
    """Test Hybrid model"""

    def test_forward_pass(self) -> None:
        """Test forward pass"""
        model = HybridModel(
            in_channels=3,
            hidden_size=128,
            num_classes=10,
            num_layers=2,
            num_heads=4,
        )
        x = torch.randn(2, 3, 32, 32)  # Batch of RGB images
        output = model(x)
        assert output.shape == (2, 10)

    def test_training_step(self) -> None:
        """Test training step"""
        model = HybridModel(
            in_channels=3,
            hidden_size=128,
            num_classes=10,
            num_layers=2,
            num_heads=4,
        )
        x = torch.randn(2, 3, 32, 32)
        y = torch.randint(0, 10, (2,))
        loss = model.training_step((x, y), 0)
        assert isinstance(loss, torch.Tensor)
        assert loss.dim() == 0  # Scalar loss


class TestBaseModelFunctionality:
    """Test base model functionality"""

    def test_optimizer_configuration(self) -> None:
        """Test optimizer configuration"""
        model = CNNModel(learning_rate=1e-4, weight_decay=1e-5)
        optimizer_config = model.configure_optimizers()

        if isinstance(optimizer_config, dict):
            assert "optimizer" in optimizer_config
        else:
            # When scheduler is "none", returns optimizer directly
            assert hasattr(optimizer_config, "param_groups")

    def test_scheduler_configuration(self) -> None:
        """Test scheduler configuration"""
        model = CNNModel(scheduler_type="cosine")
        optimizer_config = model.configure_optimizers()

        assert isinstance(optimizer_config, dict)
        assert "optimizer" in optimizer_config
        assert "lr_scheduler" in optimizer_config
