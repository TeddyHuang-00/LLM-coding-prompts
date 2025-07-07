"""
Evaluation script for trained models

This script provides a command-line interface for evaluating trained deep learning models.

Usage:
    python evaluate.py --checkpoint path/to/checkpoint.ckpt
    python evaluate.py --checkpoint path/to/checkpoint.ckpt --data-dir custom/data/path
"""

from __future__ import annotations

import argparse
import sys
import traceback
from pathlib import Path

from lightning.pytorch.utilities import rank_zero_info, rank_zero_warn

from src.config import TrainingArgs
from src.trainer import Trainer


def main() -> None:
    """Main evaluation function"""
    parser = argparse.ArgumentParser(description="Evaluate trained model")
    parser.add_argument(
        "--checkpoint", type=Path, required=True, help="Path to model checkpoint"
    )
    parser.add_argument(
        "--data-dir", type=Path, default=Path("data"), help="Path to data directory"
    )
    parser.add_argument(
        "--batch-size", type=int, default=32, help="Batch size for evaluation"
    )

    args = parser.parse_args()

    try:
        # Create minimal config for evaluation
        config = TrainingArgs()
        config.data.data_dir = args.data_dir
        config.data.batch_size = args.batch_size

        # Initialize trainer
        trainer = Trainer(config=config)
        trainer.setup_data()
        trainer.setup_trainer()

        rank_zero_info(f"Evaluating model from checkpoint: {args.checkpoint}")

        # Evaluate
        test_results = trainer.test(ckpt_path=str(args.checkpoint))

        rank_zero_info("Evaluation Results:")
        for result in test_results:
            for key, value in result.items():
                if isinstance(value, int | float):
                    rank_zero_info(f"  {key}: {value:.4f}")
                else:
                    rank_zero_info(f"  {key}: {value}")

    except KeyboardInterrupt:
        rank_zero_warn("Evaluation interrupted by user")
        sys.exit(1)
    except Exception as e:
        rank_zero_warn(f"Error during evaluation: {e}")

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
