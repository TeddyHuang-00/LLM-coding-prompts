"""Tests for configuration module"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.config import (
    AcceleratorType,
    DataConfig,
    ExperimentConfig,
    LRSchedulerType,
    ModelConfig,
    ModelType,
    PrecisionType,
    TrainingArgs,
    TrainingConfig,
)


class TestDataConfig:
    """Test DataConfig class"""

    def test_default_values(self) -> None:
        """Test default configuration values"""
        config = DataConfig()
        assert config.data_dir == Path("data")
        assert config.batch_size == 32
        assert config.num_workers == 4
        assert config.pin_memory is True
        assert config.train_split == 0.8
        assert config.val_split == 0.1
        assert config.test_split == 0.1

    def test_split_validation(self) -> None:
        """Test split ratio validation"""
        with pytest.raises(ValueError):
            DataConfig(train_split=0.0)

        with pytest.raises(ValueError):
            DataConfig(val_split=1.0)

        with pytest.raises(ValueError):
            DataConfig(test_split=-0.1)


class TestModelConfig:
    """Test ModelConfig class"""

    def test_default_values(self) -> None:
        """Test default configuration values"""
        config = ModelConfig()
        assert config.model_type == ModelType.CNN
        assert config.input_size == 784
        assert config.hidden_size == 256
        assert config.num_classes == 10
        assert config.dropout == 0.1

    def test_dropout_validation(self) -> None:
        """Test dropout validation"""
        with pytest.raises(ValueError):
            ModelConfig(dropout=-0.1)

        with pytest.raises(ValueError):
            ModelConfig(dropout=1.1)


class TestTrainingConfig:
    """Test TrainingConfig class"""

    def test_default_values(self) -> None:
        """Test default configuration values"""
        config = TrainingConfig()
        assert config.max_epochs == 100
        assert config.learning_rate == 1e-3
        assert config.weight_decay == 1e-4
        assert config.scheduler == LRSchedulerType.NONE
        assert config.patience == 10
        assert config.accelerator == AcceleratorType.AUTO
        assert config.precision == PrecisionType.FLOAT_32

    def test_positive_value_validation(self) -> None:
        """Test positive value validation"""
        with pytest.raises(ValueError):
            TrainingConfig(learning_rate=0.0)

        with pytest.raises(ValueError):
            TrainingConfig(weight_decay=-0.1)


class TestExperimentConfig:
    """Test ExperimentConfig class"""

    def test_default_values(self) -> None:
        """Test default configuration values"""
        config = ExperimentConfig()
        assert config.name == "experiment"
        assert config.output_dir == Path("outputs")
        assert config.log_every_n_steps == 10
        assert config.save_top_k == 3
        assert config.monitor == "val_loss"
        assert config.mode == "min"
        assert config.seed == 42


class TestTrainingArgs:
    """Test TrainingArgs class"""

    def test_default_values(self) -> None:
        """Test default configuration values"""
        config = TrainingArgs()
        assert isinstance(config.data, DataConfig)
        assert isinstance(config.model, ModelConfig)
        assert isinstance(config.training, TrainingConfig)
        assert isinstance(config.experiment, ExperimentConfig)

    def test_nested_config_access(self) -> None:
        """Test nested configuration access"""
        config = TrainingArgs()
        assert config.data.batch_size == 32
        assert config.model.model_type == ModelType.CNN
        assert config.training.learning_rate == 1e-3
        assert config.experiment.seed == 42
