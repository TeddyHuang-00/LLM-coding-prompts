"""Data loading utilities for deep learning training"""

from __future__ import annotations

from pathlib import Path

import lightning as L
import torch
from torch.utils.data import DataLoader, Dataset, random_split
from torchvision import transforms
from torchvision.datasets import CIFAR10, MNIST


class ExampleDataset(Dataset):
    """Example dataset for demonstration"""

    def __init__(
        self, data_dir: Path, transform: transforms.Compose | None = None
    ) -> None:
        self.data_dir = Path(data_dir)
        self.transform = transform

        # This is a placeholder - replace with your actual data loading logic
        self.data = []
        self.labels = []

        # Example: Load dummy data
        self._load_dummy_data()

    def _load_dummy_data(self) -> None:
        """Load dummy data for demonstration"""
        # Generate some dummy data
        for i in range(1000):
            # Random tensor as dummy data
            data = torch.randn(3, 32, 32)  # RGB image
            label = i % 10  # 10 classes
            self.data.append(data)
            self.labels.append(label)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, idx: int) -> tuple[torch.Tensor, torch.Tensor]:
        data = self.data[idx]
        label = self.labels[idx]

        if self.transform:
            data = self.transform(data)

        return data, torch.tensor(label, dtype=torch.long)


class DataModule(L.LightningDataModule):
    """Lightning data module for training"""

    def __init__(
        self,
        data_dir: Path,
        batch_size: int = 32,
        num_workers: int = 4,
        pin_memory: bool = True,
        train_split: float = 0.8,
        val_split: float = 0.1,
        test_split: float = 0.1,
        dataset_name: str = "example",
    ) -> None:
        super().__init__()
        self.data_dir = Path(data_dir)
        self.batch_size = batch_size
        self.num_workers = num_workers
        self.pin_memory = pin_memory
        self.train_split = train_split
        self.val_split = val_split
        self.test_split = test_split
        self.dataset_name = dataset_name

        # Transforms
        self.transform_train = transforms.Compose(
            [
                transforms.RandomHorizontalFlip(),
                transforms.RandomCrop(32, padding=4),
                (
                    transforms.ToTensor()
                    if dataset_name != "example"
                    else transforms.Lambda(lambda x: x)
                ),
                (
                    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
                    if dataset_name != "example"
                    else transforms.Lambda(lambda x: x)
                ),
            ]
        )

        self.transform_val = transforms.Compose(
            [
                (
                    transforms.ToTensor()
                    if dataset_name != "example"
                    else transforms.Lambda(lambda x: x)
                ),
                (
                    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225))
                    if dataset_name != "example"
                    else transforms.Lambda(lambda x: x)
                ),
            ]
        )

    def prepare_data(self) -> None:
        """Download data if needed"""
        if self.dataset_name == "cifar10":
            CIFAR10(self.data_dir, train=True, download=True)
            CIFAR10(self.data_dir, train=False, download=True)
        elif self.dataset_name == "mnist":
            MNIST(self.data_dir, train=True, download=True)
            MNIST(self.data_dir, train=False, download=True)

    def setup(self, stage: str | None = None) -> None:
        """Setup datasets for training/validation/testing"""
        if stage == "fit" or stage is None:
            if self.dataset_name == "cifar10":
                full_dataset = CIFAR10(
                    self.data_dir, train=True, transform=self.transform_train
                )
            elif self.dataset_name == "mnist":
                full_dataset = MNIST(
                    self.data_dir, train=True, transform=self.transform_train
                )
            else:
                full_dataset = ExampleDataset(
                    self.data_dir, transform=self.transform_train
                )

            # Split dataset
            total_size = len(full_dataset)
            train_size = int(self.train_split * total_size)
            val_size = int(self.val_split * total_size)
            test_size = total_size - train_size - val_size

            self.train_dataset, self.val_dataset, _ = random_split(
                full_dataset, [train_size, val_size, test_size]
            )

            # Create validation dataset with different transforms
            if self.dataset_name == "cifar10":
                val_full_dataset = CIFAR10(
                    self.data_dir, train=True, transform=self.transform_val
                )
            elif self.dataset_name == "mnist":
                val_full_dataset = MNIST(
                    self.data_dir, train=True, transform=self.transform_val
                )
            else:
                val_full_dataset = ExampleDataset(
                    self.data_dir, transform=self.transform_val
                )

            _, self.val_dataset, _ = random_split(
                val_full_dataset, [train_size, val_size, test_size]
            )

        if stage == "test" or stage is None:
            if self.dataset_name == "cifar10":
                self.test_dataset = CIFAR10(
                    self.data_dir, train=False, transform=self.transform_val
                )
            elif self.dataset_name == "mnist":
                self.test_dataset = MNIST(
                    self.data_dir, train=False, transform=self.transform_val
                )
            else:
                # For example dataset, use part of the data as test set
                full_dataset = ExampleDataset(
                    self.data_dir, transform=self.transform_val
                )
                total_size = len(full_dataset)
                train_size = int(self.train_split * total_size)
                val_size = int(self.val_split * total_size)
                test_size = total_size - train_size - val_size

                _, _, self.test_dataset = random_split(
                    full_dataset, [train_size, val_size, test_size]
                )

    def train_dataloader(self) -> DataLoader:
        """Return training dataloader"""
        return DataLoader(
            self.train_dataset,
            batch_size=self.batch_size,
            shuffle=True,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

    def val_dataloader(self) -> DataLoader:
        """Return validation dataloader"""
        return DataLoader(
            self.val_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )

    def test_dataloader(self) -> DataLoader:
        """Return test dataloader"""
        return DataLoader(
            self.test_dataset,
            batch_size=self.batch_size,
            shuffle=False,
            num_workers=self.num_workers,
            pin_memory=self.pin_memory,
        )
