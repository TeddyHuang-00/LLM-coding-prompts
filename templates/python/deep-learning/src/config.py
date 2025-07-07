"""
Configuration management for deep learning training

This module provides Pydantic-based configuration classes for type-safe
argument parsing and validation using pydantic-settings.
"""

from __future__ import annotations

import tomllib
from enum import Enum
from pathlib import Path

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class ModelType(str, Enum):
    """Available model architectures"""

    CNN = "cnn"
    TRANSFORMER = "transformer"
    HYBRID = "hybrid"


class AcceleratorType(str, Enum):
    """Available accelerator types"""

    AUTO = "auto"
    CPU = "cpu"
    GPU = "gpu"
    MPS = "mps"


class PrecisionType(str, Enum):
    """Available training precision types"""

    MIXED_16 = "16-mixed"
    MIXED_BF16 = "bf16-mixed"
    FLOAT_32 = "32"
    FLOAT_64 = "64"


class LRSchedulerType(str, Enum):
    """Available learning rate schedulers"""

    NONE = "none"
    STEP = "step"
    MULTISTEP = "multistep"
    COSINE = "cosine"


class DataConfig(BaseModel):
    """Data configuration"""

    data_dir: Path = Field(default=Path("data"), description="Path to data directory")
    batch_size: int = Field(default=32, description="Batch size for training")
    num_workers: int = Field(default=4, description="Number of data loader workers")
    pin_memory: bool = Field(default=True, description="Pin memory for data loading")
    train_split: float = Field(default=0.8, description="Training split ratio")
    val_split: float = Field(default=0.1, description="Validation split ratio")
    test_split: float = Field(default=0.1, description="Test split ratio")

    @field_validator("train_split", "val_split", "test_split")
    @classmethod
    def validate_splits(cls, v: float) -> float:
        """Validate split ratios"""
        if not 0 < v < 1:
            msg = "Split ratios must be between 0 and 1"
            raise ValueError(msg)
        return v


class ModelConfig(BaseModel):
    """Model configuration"""

    model_type: ModelType = Field(
        default=ModelType.CNN, description="Model architecture"
    )
    input_size: int = Field(default=784, description="Input feature size")
    hidden_size: int = Field(default=256, description="Hidden layer size")
    num_classes: int = Field(default=10, description="Number of output classes")
    dropout: float = Field(default=0.1, description="Dropout rate")

    @field_validator("dropout")
    @classmethod
    def validate_dropout(cls, v: float) -> float:
        """Validate dropout rate"""
        if not 0 <= v <= 1:
            msg = "Dropout rate must be between 0 and 1"
            raise ValueError(msg)
        return v


class TrainingConfig(BaseModel):
    """Training configuration"""

    max_epochs: int = Field(default=100, description="Maximum number of epochs")
    learning_rate: float = Field(default=1e-3, description="Learning rate")
    weight_decay: float = Field(default=1e-4, description="Weight decay")
    scheduler: LRSchedulerType = Field(
        default=LRSchedulerType.NONE, description="Learning rate scheduler"
    )
    patience: int = Field(default=10, description="Early stopping patience")
    min_delta: float = Field(
        default=0.001, description="Minimum delta for early stopping"
    )
    accelerator: AcceleratorType = Field(
        default=AcceleratorType.AUTO, description="Training accelerator"
    )
    precision: PrecisionType = Field(
        default=PrecisionType.FLOAT_32, description="Training precision"
    )
    gradient_clip_val: float = Field(default=1.0, description="Gradient clipping value")
    accumulate_grad_batches: int = Field(
        default=1, description="Gradient accumulation steps"
    )

    @field_validator("learning_rate", "weight_decay")
    @classmethod
    def validate_positive(cls, v: float) -> float:
        """Validate positive values"""
        if v <= 0:
            msg = "Value must be positive"
            raise ValueError(msg)
        return v


class ExperimentConfig(BaseModel):
    """Experiment configuration"""

    name: str = Field(default="experiment", description="Experiment name")
    config: Path | None = Field(default=None, description="Path to configuration file")
    output_dir: Path = Field(default=Path("outputs"), description="Output directory")
    log_every_n_steps: int = Field(default=10, description="Logging frequency")
    val_check_interval: float = Field(
        default=1.0, description="Validation check interval"
    )
    save_top_k: int = Field(default=3, description="Number of best checkpoints to save")
    monitor: str = Field(default="val_loss", description="Metric to monitor")
    mode: str = Field(default="min", description="Monitor mode (min/max)")
    seed: int = Field(default=42, description="Random seed")


class TrainingArgs(BaseSettings):
    """Main training arguments"""

    """Complete training configuration combining all sub-configurations"""

    model_config = SettingsConfigDict(
        env_prefix="PRECICE_",  # Environment variables prefix
        env_nested_delimiter="__",  # For nested configs like PRECICE_MODEL__DROPOUT
        case_sensitive=False,
        extra="forbid",  # Prevent extra fields
        validate_assignment=True,  # Validate on assignment
        use_enum_values=True,  # Use enum values instead of enum objects
        cli_parse_args=True,  # Enable CLI argument parsing
        cli_implicit_flags=True,  # Allow implicit flags in CLI
        cli_kebab_case=True,  # Use kebab-case for CLI arguments
        cli_avoid_json=True,  # Avoid JSON parsing for CLI
        cli_use_class_docs_for_groups=True,  # Use class docstrings for CLI help
    )

    data: DataConfig = Field(default_factory=DataConfig)
    model: ModelConfig = Field(default_factory=ModelConfig)
    training: TrainingConfig = Field(default_factory=TrainingConfig)
    experiment: ExperimentConfig = Field(default_factory=ExperimentConfig)

    @classmethod
    def create_from_cli(cls) -> TrainingArgs:
        """Create configuration from command line arguments"""
        # environment variable loading + CLI parsing
        instance = cls()

        # Load configuration from file if specified
        if instance.experiment.config is not None:
            with instance.experiment.config.open("rb") as f:
                config_data = tomllib.load(f)
            instance = cls(**config_data)

        return instance

    def print_config(self) -> None:
        """Print configuration in a readable format"""
        print("=" * 50)
        print("Training Configuration")
        print("=" * 50)

        sections = [
            ("Data", self.data),
            ("Model", self.model),
            ("Training", self.training),
            ("Experiment", self.experiment),
        ]

        for section_name, config in sections:
            print(f"\n{section_name}:")
            for key, value in config.model_dump().items():
                print(f"  {key}: {value}")

        print("=" * 50)
