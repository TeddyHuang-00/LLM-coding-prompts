# Deep Learning Template

A modern deep learning project template built with PyTorch Lightning, featuring best practices for model development, training, and evaluation.

## Features

- **PyTorch Lightning**: Simplified training loop with built-in best practices
- **Multiple Model Architectures**: CNN, Transformer, and Hybrid models
- **Type-Safe Configuration**: Pydantic-based configuration with CLI support
- **Modern Python**: Python 3.12+ with type hints and modern tooling
- **Testing**: Comprehensive test suite with pytest
- **Code Quality**: Pre-commit hooks, ruff linting, and mypy type checking
- **Visualization**: Training plots and model analysis utilities

## Project Structure

```
{{PROJECT_NAME}}/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py           # Base model class
│   │   ├── cnn.py            # CNN implementation
│   │   ├── transformer.py    # Transformer implementation
│   │   └── hybrid.py         # Hybrid CNN-Transformer
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── metrics.py        # Evaluation metrics
│   │   └── visualization.py  # Plotting utilities
│   ├── config.py             # Configuration classes
│   ├── dataloader.py         # Data loading utilities
│   └── trainer.py            # Training orchestrator
├── tests/
│   ├── test_config.py        # Configuration tests
│   └── test_models.py        # Model tests
├── config/
│   └── example.toml          # Example configuration
├── train.py                  # Training script
├── evaluate.py               # Evaluation script
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Quick Start

### 1. Install Dependencies

```bash
# Install the project in development mode
pip install -e ".[dev]"

# Or install specific extra dependencies
pip install -e ".[dev,vision,nlp,data]"
```

### 2. Basic Training

```bash
# Train a CNN model
python train.py --model-model-type cnn --training-max-epochs 50

# Train a Transformer model
python train.py --model-model-type transformer --training-learning-rate 1e-4

# Train with custom configuration
python train.py --experiment-name my_experiment --data-batch-size 64
```

### 3. Evaluation

```bash
# Evaluate trained model
python evaluate.py --checkpoint outputs/my_experiment/checkpoints/best.ckpt
```

## Configuration

The project uses Pydantic for type-safe configuration. You can configure training in three ways:

### 1. Command Line Arguments

```bash
python train.py \
    --model-model-type cnn \
    --model-hidden-size 512 \
    --training-learning-rate 1e-3 \
    --training-max-epochs 100 \
    --experiment-name my_cnn_experiment
```

### 2. Environment Variables

```bash
export TRAIN_MODEL__MODEL_TYPE=transformer
export TRAIN_TRAINING__LEARNING_RATE=1e-4
python train.py
```

### 3. Configuration Files

Create a TOML file (see `config/example.toml`) and modify the code to load it:

```python
# In your training script
from src.config import TrainingArgs

# Load from file (you'll need to implement this)
config = TrainingArgs.from_toml("config/my_config.toml")
```

## Available Models

### CNN Model
- Simple convolutional neural network
- Suitable for image classification tasks
- Configurable depth and width

### Transformer Model
- Self-attention based architecture
- Suitable for sequence modeling tasks
- Configurable layers, heads, and dimensions

### Hybrid Model
- Combines CNN feature extraction with Transformer processing
- Suitable for tasks requiring both spatial and sequential modeling
- Best of both architectures

## Model Configuration

Each model type supports various configuration options:

```python
# CNN Model
model_config = {
    "model_type": "cnn",
    "in_channels": 3,        # RGB images
    "num_classes": 10,       # Number of output classes
    "hidden_size": 64,       # Base hidden dimension
}

# Transformer Model
model_config = {
    "model_type": "transformer",
    "input_size": 512,       # Input feature dimension
    "num_classes": 10,       # Number of output classes
    "hidden_size": 256,      # Model dimension
    "num_layers": 6,         # Number of transformer layers
    "num_heads": 8,          # Number of attention heads
}

# Hybrid Model
model_config = {
    "model_type": "hybrid",
    "in_channels": 3,        # Input channels
    "num_classes": 10,       # Number of output classes
    "hidden_size": 256,      # Model dimension
    "num_layers": 4,         # Number of transformer layers
    "num_heads": 8,          # Number of attention heads
}
```

## Training Configuration

Configure training parameters:

```python
training_config = {
    "max_epochs": 100,
    "learning_rate": 1e-3,
    "weight_decay": 1e-4,
    "scheduler": "cosine",           # "none", "step", "multistep", "cosine"
    "accelerator": "auto",           # "auto", "cpu", "gpu", "mps"
    "precision": "32",               # "32", "16-mixed", "bf16-mixed"
    "gradient_clip_val": 1.0,
    "accumulate_grad_batches": 1,
}
```

## Data Loading

The template includes a flexible data loading system:

```python
from src.dataloader import DataModule

# Create data module
data_module = DataModule(
    data_dir="path/to/data",
    batch_size=32,
    num_workers=4,
    train_split=0.8,
    val_split=0.1,
    test_split=0.1,
    dataset_name="cifar10",  # "cifar10", "mnist", or "example"
)
```

### Supported Datasets

- **CIFAR-10**: Automatic download and preprocessing
- **MNIST**: Automatic download and preprocessing
- **Custom**: Implement your own dataset class

## Development

### Code Quality

```bash
# Install pre-commit hooks
pre-commit install

# Run linting
ruff check src/ tests/
ruff format src/ tests/

# Run type checking
mypy src/

# Run tests
pytest tests/
```

### Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test categories
pytest -m "not slow"  # Skip slow tests
pytest -m "unit"      # Run only unit tests
```

### Adding New Models

1. Create a new model file in `src/models/`
2. Inherit from `BaseModel`
3. Implement the `_build_model` method
4. Register in `src/models/__init__.py`
5. Add tests in `tests/test_models.py`

Example:

```python
from src.models.base import BaseModel
import torch.nn as nn

class MyModel(BaseModel):
    def _build_model(self, **kwargs):
        return nn.Sequential(
            nn.Linear(kwargs.get("input_size", 784), 128),
            nn.ReLU(),
            nn.Linear(128, kwargs.get("num_classes", 10)),
        )
```

## Monitoring and Logging

The template includes comprehensive logging:

- **CSV Logger**: Training metrics saved to CSV files
- **Model Checkpointing**: Automatic saving of best models
- **Early Stopping**: Prevent overfitting
- **Learning Rate Monitoring**: Track learning rate changes

Logs are saved to `outputs/{experiment_name}/logs/`

## Best Practices

1. **Use Type Hints**: All code includes comprehensive type hints
2. **Configuration Management**: Use Pydantic for type-safe configuration
3. **Testing**: Write tests for all components
4. **Code Quality**: Use pre-commit hooks and linting
5. **Documentation**: Document all functions and classes
6. **Reproducibility**: Set seeds and use deterministic training
7. **Monitoring**: Log metrics and use early stopping

## Customization

### Custom Loss Functions

```python
# In your model class
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.criterion = nn.CrossEntropyLoss(weight=class_weights)
```

### Custom Metrics

```python
# Add to training_step, validation_step, test_step
from torchmetrics import Accuracy, F1Score

self.accuracy = Accuracy(num_classes=num_classes)
self.f1_score = F1Score(num_classes=num_classes)
```

### Custom Callbacks

```python
# In trainer.py
from lightning.pytorch.callbacks import Callback

class MyCallback(Callback):
    def on_epoch_end(self, trainer, pl_module):
        # Custom logic here
        pass

# Add to trainer callbacks
callbacks.append(MyCallback())
```

## License

This template is released under the MIT License. See the LICENSE file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Troubleshooting

### Common Issues

1. **CUDA Out of Memory**: Reduce batch size or use gradient accumulation
2. **Slow Training**: Increase num_workers or use faster data loading
3. **Model Not Learning**: Check learning rate, try different optimizers
4. **Validation Loss Increasing**: Use early stopping or regularization

### Performance Tips

1. **Use Mixed Precision**: Set `precision="16-mixed"` for faster training
2. **Optimize Data Loading**: Use `pin_memory=True` and appropriate `num_workers`
3. **Gradient Accumulation**: Use `accumulate_grad_batches` for larger effective batch sizes
4. **Model Compilation**: Use `torch.compile()` for PyTorch 2.0+

## Resources

- [PyTorch Lightning Documentation](https://pytorch-lightning.readthedocs.io/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)