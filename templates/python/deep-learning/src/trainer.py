"""Training utilities for deep learning models"""

from __future__ import annotations

from typing import Any

import lightning as L
import torch
from lightning.pytorch.callbacks import (
    EarlyStopping,
    LearningRateMonitor,
    ModelCheckpoint,
)
from lightning.pytorch.loggers import CSVLogger

from .config import TrainingArgs
from .dataloader import DataModule
from .models import create_model


class Trainer:
    """Training orchestrator"""

    def __init__(self, config: TrainingArgs) -> None:
        self.config = config
        self.data_module = None
        self.model = None
        self.trainer = None

    def setup_data(self) -> None:
        """Setup data module"""
        self.data_module = DataModule(
            data_dir=self.config.data.data_dir,
            batch_size=self.config.data.batch_size,
            num_workers=self.config.data.num_workers,
            pin_memory=self.config.data.pin_memory,
            train_split=self.config.data.train_split,
            val_split=self.config.data.val_split,
            test_split=self.config.data.test_split,
        )

    def setup_model(self) -> None:
        """Setup model"""
        self.model = create_model(
            model_type=self.config.model.model_type.value,
            input_size=self.config.model.input_size,
            hidden_size=self.config.model.hidden_size,
            num_classes=self.config.model.num_classes,
            dropout=self.config.model.dropout,
            learning_rate=self.config.training.learning_rate,
            weight_decay=self.config.training.weight_decay,
            scheduler_type=self.config.training.scheduler.value,
        )

    def setup_trainer(self) -> None:
        """Setup Lightning trainer"""
        # Create output directory
        output_dir = self.config.experiment.output_dir / self.config.experiment.name
        output_dir.mkdir(parents=True, exist_ok=True)

        # Callbacks
        callbacks = [
            ModelCheckpoint(
                dirpath=output_dir / "checkpoints",
                monitor=self.config.experiment.monitor,
                mode=self.config.experiment.mode,
                save_top_k=self.config.experiment.save_top_k,
                save_last=True,
                filename="{epoch}-{val_loss:.2f}",
            ),
            EarlyStopping(
                monitor=self.config.experiment.monitor,
                mode=self.config.experiment.mode,
                patience=self.config.training.patience,
                min_delta=self.config.training.min_delta,
            ),
            LearningRateMonitor(logging_interval="epoch"),
        ]

        # Logger
        logger = CSVLogger(
            save_dir=output_dir / "logs",
            name="training",
        )

        # Trainer
        self.trainer = L.Trainer(
            max_epochs=self.config.training.max_epochs,
            accelerator=self.config.training.accelerator.value,
            precision=self.config.training.precision.value,
            gradient_clip_val=self.config.training.gradient_clip_val,
            accumulate_grad_batches=self.config.training.accumulate_grad_batches,
            log_every_n_steps=self.config.experiment.log_every_n_steps,
            val_check_interval=self.config.experiment.val_check_interval,
            callbacks=callbacks,
            logger=logger,
            deterministic=True,
            enable_checkpointing=True,
            enable_progress_bar=True,
            enable_model_summary=True,
        )

    def train(self) -> None:
        """Train the model"""
        if self.trainer is None or self.model is None or self.data_module is None:
            msg = "Trainer, model, or data module not setup. Call setup methods first."
            raise RuntimeError(msg)

        # Set seed for reproducibility
        L.seed_everything(self.config.experiment.seed)

        # Train
        self.trainer.fit(self.model, self.data_module)

    def test(self, ckpt_path: str | None = None) -> list[dict[str, Any]]:
        """Test the model"""
        if self.trainer is None or self.data_module is None:
            msg = "Trainer or data module not setup. Call setup methods first."
            raise RuntimeError(msg)

        return self.trainer.test(self.model, self.data_module, ckpt_path=ckpt_path)

    def predict(self, data: torch.Tensor) -> torch.Tensor:
        """Make predictions"""
        if self.model is None:
            msg = "Model not setup. Call setup_model first."
            raise RuntimeError(msg)

        self.model.eval()
        with torch.no_grad():
            return self.model(data)
