# Python Development Guide

Use Python 3.12+ with uv for dependency management, Ruff for linting/formatting, and Pydantic-settings for configuration.

## Dependency Management

**ALWAYS use `uv` exclusively for Python dependency management.**

### Setup

```bash
# Add dependencies
uv add fastapi pydantic-settings
uv add --dev pytest ruff mypy

# Install dependencies
uv sync
```

### Essential uv Commands

```bash
uv add package-name              # Add dependency
uv add --dev package-name        # Add dev dependency
uv remove package-name           # Remove dependency
uv sync                          # Install/update all dependencies
uv run python main.py            # Run with uv environment
uv run pytest                    # Run tests
uv run ruff check .              # Run linting
```

## Code Quality

**ALWAYS use Ruff for linting/formatting and mypy for type checking.**

Use the project templates which include complete configurations for:
- Ruff linting rules and formatting
- mypy strict type checking  
- pytest configuration with coverage

### Essential Commands

```bash
uv run ruff check --fix .     # Fix auto-fixable issues
uv run ruff format .          # Format code
uv run ruff check . --diff    # Show what would change
uv run mypy .                 # Type check all files
uv run mypy --install-types   # Install missing type stubs
```

## Pydantic Settings

Type-safe configuration management with automatic validation.

### Basic Setup

```python
from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_"
    )

    # Basic fields
    app_name: str = "My App"
    debug: bool = False

    # With validation
    port: int = Field(default=8000, ge=1, le=65535)

    # Secrets
    secret_key: SecretStr = Field(description="App secret")

    # Lists from env: APP_ALLOWED_HOSTS=["localhost","127.0.0.1"]
    allowed_hosts: list[str] = Field(default_factory=list)

# Usage
settings = Settings()
print(settings.secret_key.get_secret_value())  # Access secret
```

### Nested Configuration

```python
class DatabaseConfig(BaseSettings):
    host: str = "localhost"
    port: int = 5432
    username: str
    password: SecretStr

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__"
    )

    database: DatabaseConfig = Field(default_factory=DatabaseConfig)

# Environment: DB__HOST=prod.db.com DB__PORT=5433
settings = Settings()
```

## FastAPI Integration

```python
from functools import lru_cache
from fastapi import FastAPI, Depends

@lru_cache
def get_settings():
    return Settings()

app = FastAPI()

@app.get("/")
async def root(settings: Settings = Depends(get_settings)):
    return {"app": settings.app_name}
```

## CI/CD & Development

Use the project templates which include complete configurations for:
- GitHub Actions CI/CD with uv
- Coverage reporting and code quality checks

## Best Practices

### Code Quality

- **ALWAYS run full quality checks after each modification**:
  ```bash
  uv run ruff check --fix .
  uv run ruff format .
  uv run mypy .
  uv run pytest
  ```
- **Run these checks immediately after making any code changes**
- Use type hints for all function parameters and returns
- Keep functions small and focused
- Write docstrings for public APIs
- Use `@lru_cache` for expensive computations
- Use `from __future__ import annotations` for forward references

### Project Structure

```
project/
├── src/
│   └── mypackage/
│       ├── __init__.py
│       ├── main.py
│       └── config.py
├── tests/
├── pyproject.toml
├── uv.lock
└── .python-version
```

### Development Workflow

1. **Project Setup**:

   ```bash
   uv init project-name
   cd project-name
   uv add --dev ruff mypy pytest pytest-cov
   ```

2. **Daily Development**:

   ```bash
   uv sync                    # Update dependencies
   uv run ruff check --fix .  # Fix linting issues
   uv run mypy .              # Check types
   uv run pytest             # Run tests
   ```

3. **After Each Modification** (run immediately):
   ```bash
   uv run ruff check . && uv run ruff format . && uv run mypy . && uv run pytest
   ```

### Testing

```python
import pytest
from mypackage.config import Settings

def test_settings_load():
    settings = Settings()
    assert settings.app_name
    assert settings.port > 0
```

### Environment Files

```bash
# .env
APP_NAME=My Application
APP_DEBUG=true
APP_PORT=8000
APP_SECRET_KEY=your-secret-here
```
