"""
Main training script for deep learning models

This script provides a command-line interface for training deep learning models
with PyTorch Lightning. It supports different model architectures and flexible
configuration.

Usage:
    python train.py --model-model-type cnn --training-max-epochs 100
    python train.py --model-model-type transformer --training-learning-rate 1e-4
    python train.py --experiment-name my_experiment
"""

from __future__ import annotations

import sys
import traceback

from lightning.pytorch.utilities import rank_zero_info, rank_zero_warn

from src.config import TrainingArgs
from src.trainer import Trainer


def main() -> None:
    """Main training function"""
    args = TrainingArgs.create_from_cli()

    args.print_config()

    try:
        # Initialize trainer
        trainer = Trainer(config=args)
        trainer.setup_data()
        trainer.setup_model()
        trainer.setup_trainer()

        rank_zero_info("Starting training...")
        trainer.train()
        rank_zero_info("Training completed successfully!")

        # Run test evaluation
        rank_zero_info("Running final evaluation on test set...")
        test_results = trainer.test()
        rank_zero_info("Final Test Results:")
        for result in test_results:
            for key, value in result.items():
                if isinstance(value, int | float):
                    rank_zero_info(f"  {key}: {value:.4f}")
                else:
                    rank_zero_info(f"  {key}: {value}")

    except KeyboardInterrupt:
        rank_zero_warn("Training interrupted by user")
        sys.exit(1)
    except Exception as e:
        rank_zero_warn(f"Error during training: {e}")

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
