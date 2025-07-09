# {{PROJECT_NAME}}

A modern Python project template with comprehensive tooling and best practices.

## Features

- **Modern Python**: Targets Python 3.11+ with modern syntax and features
- **Ruff**: Ultra-fast linting and formatting (10-100x faster than traditional tools)
- **Pydantic Settings**: Type-safe configuration management
- **Comprehensive Testing**: pytest with coverage reporting
- **Type Checking**: mypy with strict configuration
- **Developer Experience**: Pre-configured development environment

## Setup

1. **Install UV**:
   ```bash
   uv --version  # Should be 0.7+
   ```
2. **Install dependencies**:
   ```bash
   uv sync
   ```

## Development

### Code Quality

Run all quality checks:

```bash
# Format code
ruff format

# Lint code
ruff check --fix

# Type check
mypy src/

# Run tests
pytest

# All checks together
ruff format && ruff check && mypy src/ && pytest
```

### Project Structure

```
{{PROJECT_NAME}}/
├── src/                # Source code
│   └── main.py         # Main entry point
├── tests/              # Test files
├── pyproject.toml      # Project configuration
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

## Configuration

The project uses `pyproject.toml` for all tool configuration:

- **Ruff**: Linting and formatting with comprehensive rules
- **mypy**: Strict type checking
- **pytest**: Test configuration with coverage
- **Build system**: Hatchling for modern Python packaging

## Usage

Run the application:

```bash
uv run src/main.py
```

## Dependencies

- **Core**: pydantic-settings for configuration management
- **Dev**: ruff, pytest, mypy for development tooling

## Best Practices

This template follows modern Python best practices:

- **Type hints**: All code uses proper type annotations
- **Import organization**: Imports are organized and formatted consistently
- **Error handling**: Proper exception handling patterns
- **Documentation**: Clear docstrings and comments
- **Testing**: Comprehensive test coverage
- **Code quality**: Zero linting warnings and strict type checking

## License

{{LICENSE_TEXT}}
