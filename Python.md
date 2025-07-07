# Modern Python Development with Ruff and Pydantic-Settings

**Ruff has revolutionized Python tooling with 10-100x performance improvements over traditional tools, while Pydantic-settings provides type-safe configuration management that scales from development to enterprise production environments**. Together, they form a powerful foundation for modern Python development workflows that prioritize speed, type safety, and developer experience.

The combination of Ruff's unified linting/formatting capabilities with Pydantic-settings' robust configuration management addresses the most common pain points in Python development: slow tooling, fragmented configuration, and lack of type safety. This comprehensive guide covers the latest best practices, advanced configurations, and production-ready patterns for Python 3.11+ development.

## Ruff as the exclusive Python development tool

Ruff consolidates multiple tools into a single, blazingly fast solution. Built in Rust, it delivers **sub-second feedback loops** even on codebases with 250,000+ lines of code. The tool replaces Black, isort, Flake8, pyupgrade, autoflake, and dozens of other tools while maintaining compatibility with existing workflows.

### Complete pyproject.toml configuration

```toml
[tool.ruff]
# Global settings for Python 3.11+ projects
line-length = 88
indent-width = 4
target-version = "py311"
preview = true  # Enable latest features

# File discovery and exclusions
include = ["*.py", "*.pyi", "*.ipynb"]
exclude = [
    ".git", ".venv", "__pycache__", "build", "dist",
    "migrations", "node_modules", ".pytest_cache"
]

# Project structure
src = ["src", "tests"]

[tool.ruff.lint]
# Comprehensive rule set for modern Python
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "N",    # pep8-naming
    "D",    # pydocstyle
    "UP",   # pyupgrade
    "ANN",  # flake8-annotations
    "ASYNC", # flake8-async
    "S",    # flake8-bandit (security)
    "BLE",  # flake8-blind-except
    "B",    # flake8-bugbear
    "A",    # flake8-builtins
    "COM",  # flake8-commas
    "C4",   # flake8-comprehensions
    "DTZ",  # flake8-datetimez
    "T10",  # flake8-debugger
    "EM",   # flake8-errmsg
    "FA",   # flake8-future-annotations
    "ISC",  # flake8-implicit-str-concat
    "ICN",  # flake8-import-conventions
    "G",    # flake8-logging-format
    "INP",  # flake8-no-pep420
    "PIE",  # flake8-pie
    "T20",  # flake8-print
    "PT",   # flake8-pytest-style
    "Q",    # flake8-quotes
    "RSE",  # flake8-raise
    "RET",  # flake8-return
    "SLF",  # flake8-self
    "SIM",  # flake8-simplify
    "TID",  # flake8-tidy-imports
    "ARG",  # flake8-unused-arguments
    "PTH",  # flake8-use-pathlib
    "TD",   # flake8-todos
    "FIX",  # flake8-fixme
    "PERF", # Perflint
    "FURB", # refurb
    "LOG",  # flake8-logging
    "RUF",  # Ruff-specific rules
    "C90",  # mccabe complexity
    "PL",   # Pylint
    "TRY",  # tryceratops
]

# Rules to ignore for practical development
ignore = [
    "E501",   # Line length (handled by formatter)
    "D100",   # Missing docstring in public module
    "D101",   # Missing docstring in public class
    "D102",   # Missing docstring in public method
    "D103",   # Missing docstring in public function
    "D104",   # Missing docstring in public package
    "COM812", # Trailing comma missing (handled by formatter)
    "ISC001", # String concatenation (handled by formatter)
]

# Auto-fix configuration
fixable = ["ALL"]
unfixable = []

# Per-file ignores for different contexts
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["E402", "F401"]
"tests/*" = ["D", "S101", "ARG", "PLR2004"]
"scripts/*" = ["T20"]
"**/migrations/*" = ["ALL"]

# Advanced import sorting
[tool.ruff.lint.isort]
known-first-party = ["myproject"]
known-third-party = ["requests", "pandas", "numpy"]
section-order = ["future", "standard-library", "third-party", "first-party", "local-folder"]
required-imports = ["from __future__ import annotations"]
force-single-line = false
force-sort-within-sections = true
combine-as-imports = true

# Plugin-specific configurations
[tool.ruff.lint.flake8-annotations]
mypy-init-return = true
suppress-dummy-args = true
suppress-none-returning = true

[tool.ruff.lint.flake8-bugbear]
extend-immutable-calls = ["fastapi.Depends", "pydantic.Field"]

[tool.ruff.lint.flake8-quotes]
docstring-quotes = "double"
inline-quotes = "double"

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.mccabe]
max-complexity = 10

# Formatting configuration
[tool.ruff.format]
quote-style = "double"
indent-style = "space"
skip-magic-trailing-comma = false
line-ending = "auto"
docstring-code-format = true
docstring-code-line-length = "dynamic"
```

### Performance optimization strategies

Ruff's architecture delivers exceptional performance through intelligent caching, parallel processing, and Rust-based implementation. **Benchmark results show 150-200x speed improvements** over Flake8 and 2-3x improvements over Black on large codebases.

```toml
# Performance-optimized configuration
[tool.ruff]
cache-dir = ".ruff_cache"
respect-gitignore = true

# Exclude patterns for optimal performance
extend-exclude = [
    "legacy_code/",
    "third_party/",
    "generated/",
    "*.pb2.py",
    "*_pb2.py",
]

# Selective rule application for speed
[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]  # Unused imports
"tests/*" = ["D", "S101", "PLR2004"]  # Skip docs/security in tests
"scripts/*" = ["T20", "S"]  # Allow prints in scripts
```

## Pydantic-settings for modern configuration management

Pydantic-settings v2.x provides enterprise-grade configuration management with **type-safe validation, hierarchical structures, and multi-source loading capabilities**. It seamlessly integrates with modern Python applications and cloud-native deployment patterns.

### Advanced configuration patterns

```python
from pydantic import Field, SecretStr, computed_field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Self, Literal
from enum import Enum

class LogLevel(str, Enum):
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class DatabaseConfig(BaseSettings):
    """Database configuration with validation."""

    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, ge=1, le=65535)
    username: str = Field(description="Database username")
    password: SecretStr = Field(description="Database password")
    database: str = Field(description="Database name")
    pool_size: int = Field(default=10, ge=1, le=100)
    max_overflow: int = Field(default=20, ge=0)

    @computed_field
    @property
    def connection_string(self) -> str:
        """Generate database connection string."""
        pwd = self.password.get_secret_value()
        return f"postgresql://{self.username}:{pwd}@{self.host}:{self.port}/{self.database}"

    @field_validator('host')
    @classmethod
    def validate_host(cls, v: str) -> str:
        if not v or v.isspace():
            raise ValueError('Database host cannot be empty')
        return v.strip()

class RedisConfig(BaseSettings):
    """Redis configuration for caching."""

    host: str = Field(default="localhost")
    port: int = Field(default=6379, ge=1, le=65535)
    password: SecretStr | None = Field(default=None)
    database: int = Field(default=0, ge=0, le=15)
    max_connections: int = Field(default=20, ge=1)

class AppSettings(BaseSettings):
    """Main application settings with nested configuration."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        env_prefix="APP_",
        case_sensitive=False,
        validate_default=True,
        extra="ignore"
    )

    # Application settings
    app_name: str = Field(default="Modern Python App")
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = Field(default=False)
    log_level: LogLevel = Field(default=LogLevel.INFO)

    # Security settings
    secret_key: SecretStr = Field(description="Application secret key")
    allowed_hosts: list[str] = Field(default_factory=list)

    # Feature flags
    feature_flags: dict[str, bool] = Field(default_factory=dict)

    # Nested configurations
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)

    @computed_field
    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    @computed_field
    @property
    def effective_log_level(self) -> str:
        if self.debug:
            return LogLevel.DEBUG.value
        return self.log_level.value

    @field_validator('allowed_hosts')
    @classmethod
    def validate_hosts(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("ALLOWED_HOSTS must be configured")
        return v
```

### Environment variable mapping

```bash
# Environment variables for nested configuration
APP_ENVIRONMENT=production
APP_DEBUG=false
APP_LOG_LEVEL=info
APP_SECRET_KEY=your-secret-key-here
APP_ALLOWED_HOSTS=["example.com", "api.example.com"]

# Database configuration
APP_DATABASE__HOST=db.example.com
APP_DATABASE__PORT=5432
APP_DATABASE__USERNAME=myuser
APP_DATABASE__PASSWORD=secure-password
APP_DATABASE__DATABASE=myapp

# Redis configuration
APP_REDIS__HOST=redis.example.com
APP_REDIS__PASSWORD=redis-password
APP_REDIS__MAX_CONNECTIONS=30

# Feature flags
APP_FEATURE_FLAGS={"new_ui": true, "beta_features": false}
```

### Multi-source configuration loading

```python
from pydantic_settings import PydanticBaseSettingsSource, BaseSettings
from typing import Any, Dict, Tuple, Type
import json
import yaml

class DatabaseSettingsSource(PydanticBaseSettingsSource):
    """Load settings from database or external service."""

    def get_field_value(self, field_info, field_name: str) -> tuple[Any, str, bool]:
        # Custom logic for external configuration retrieval
        if field_name in ['api_key', 'database_password']:
            value = self._fetch_from_vault(field_name)
            return value, field_name, True
        return None, field_name, False

    def _fetch_from_vault(self, field_name: str) -> str:
        # Implementation for HashiCorp Vault, AWS Secrets Manager, etc.
        pass

class ProductionSettings(BaseSettings):
    """Production-ready settings with multiple sources."""

    model_config = SettingsConfigDict(
        env_file=[".env.local", ".env.production", ".env"],
        yaml_file="config.yaml",
        json_file="config.json"
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            DatabaseSettingsSource(settings_cls),
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
```

## Integration with modern Python workflows

### CI/CD pipeline integration

```yaml
# .github/workflows/ci.yml
name: Python CI
on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff pytest

      - name: Run Ruff linting
        run: |
          ruff check --output-format=github --show-fixes .

      - name: Run Ruff formatting
        run: |
          ruff format --check --diff .

      - name: Run tests
        run: |
          pytest
```

### Pre-commit hooks configuration

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.12.2
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [types-requests]
```

### FastAPI application integration

```python
from fastapi import FastAPI, Depends
from functools import lru_cache
from pydantic_settings import BaseSettings

class APISettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    app_name: str = "FastAPI Application"
    admin_email: str = Field(description="Administrator email")
    database_url: str = Field(description="Database connection URL")
    redis_url: str = Field(description="Redis connection URL")
    secret_key: SecretStr = Field(description="JWT secret key")

    # Performance settings
    max_connections: int = Field(default=100, ge=1)
    connection_timeout: int = Field(default=30, ge=1)

@lru_cache(maxsize=1)
def get_settings() -> APISettings:
    """Cached settings instance for optimal performance."""
    return APISettings()

app = FastAPI()

@app.get("/")
async def root(settings: APISettings = Depends(get_settings)):
    return {"app_name": settings.app_name}

@app.get("/health")
async def health_check(settings: APISettings = Depends(get_settings)):
    return {
        "status": "healthy",
        "environment": settings.environment,
        "database_connected": True  # Add actual health checks
    }
```

## Production deployment patterns

### Container and Kubernetes deployment

```dockerfile
# Multi-stage Dockerfile with Ruff
FROM python:3.11-slim as builder

# Install Ruff for build-time checks
RUN pip install ruff

# Copy source code
COPY . /app
WORKDIR /app

# Run code quality checks
RUN ruff check --output-format=json . > /app/ruff-report.json
RUN ruff format --check .

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim as runtime

# Copy application and dependencies
COPY --from=builder /app /app
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

WORKDIR /app

# Create non-root user
RUN useradd --create-home --shell /bin/bash app
USER app

CMD ["python", "main.py"]
```

### Kubernetes configuration management

```yaml
# kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
  namespace: production
data:
  APP_ENVIRONMENT: "production"
  APP_LOG_LEVEL: "INFO"
  APP_DATABASE__HOST: "postgres.database.svc.cluster.local"
  APP_DATABASE__PORT: "5432"
  APP_REDIS__HOST: "redis.cache.svc.cluster.local"

---
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
  namespace: production
type: Opaque
data:
  APP_SECRET_KEY: <base64-encoded-secret>
  APP_DATABASE__PASSWORD: <base64-encoded-password>
  APP_REDIS__PASSWORD: <base64-encoded-password>
```

## Performance optimization techniques

### Ruff performance characteristics

**Ruff consistently delivers 10-100x performance improvements** over traditional Python tooling combinations. Key performance metrics include:

- **Small codebases**: 0.1-0.2 seconds vs 5-10 seconds (25-100x faster)
- **Medium codebases**: 0.2-0.5 seconds vs 20-60 seconds (40-300x faster)
- **Large codebases**: 0.4-1.0 seconds vs 2-5 minutes (100-750x faster)

### Pydantic-settings optimization

```python
from functools import lru_cache
from pydantic_settings import BaseSettings

class OptimizedSettings(BaseSettings):
    """Performance-optimized settings with caching."""

    model_config = SettingsConfigDict(
        env_file=".env",
        validate_assignment=True,
        defer_build=True,  # Lazy loading
        nested_model_default_partial_update=True
    )

@lru_cache(maxsize=1)
def get_cached_settings() -> OptimizedSettings:
    """Singleton settings instance with caching."""
    return OptimizedSettings()

# Usage in production applications
settings = get_cached_settings()
```

## Advanced enterprise features

### Security and secret management

```python
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings
import os

class SecureSettings(BaseSettings):
    """Enterprise security configuration."""

    model_config = SettingsConfigDict(
        secrets_dir="/run/secrets",  # Docker/Kubernetes secrets
        env_file=".env",
        case_sensitive=True
    )

    # Security settings
    secret_key: SecretStr = Field(description="Application secret key")
    database_password: SecretStr = Field(description="Database password")
    api_key: SecretStr = Field(description="External API key")

    # TLS configuration
    tls_cert_path: str = Field(default="/etc/ssl/certs/app.crt")
    tls_key_path: str = Field(default="/etc/ssl/private/app.key")

    # Rate limiting
    rate_limit_requests: int = Field(default=100, ge=1)
    rate_limit_window: int = Field(default=60, ge=1)

    # CORS configuration
    cors_origins: list[str] = Field(default_factory=list)
    allowed_hosts: list[str] = Field(default_factory=list)

# AWS Secrets Manager integration
class AWSSecretsSettings(BaseSettings):
    """Integration with AWS Secrets Manager."""

    model_config = SettingsConfigDict(
        secrets_name="production/app/secrets",
        aws_region="us-east-1"
    )

    database_password: SecretStr
    api_key: SecretStr
    jwt_secret: SecretStr
```

### Monitoring and observability

```python
import structlog
from pydantic_settings import BaseSettings
from pydantic import Field

class ObservableSettings(BaseSettings):
    """Settings with built-in observability."""

    model_config = SettingsConfigDict(
        env_file=".env",
        validate_assignment=True
    )

    log_level: str = Field(default="INFO")
    metrics_enabled: bool = Field(default=True)
    tracing_enabled: bool = Field(default=True)

    def model_post_init(self, __context):
        """Log configuration loading with structured logging."""
        logger = structlog.get_logger()
        logger.info(
            "Configuration loaded",
            log_level=self.log_level,
            metrics_enabled=self.metrics_enabled,
            tracing_enabled=self.tracing_enabled,
            source="pydantic-settings"
        )
```

## Migration strategies and best practices

### Adopting Ruff incrementally

```toml
# Phase 1: Core rules only
[tool.ruff.lint]
select = ["E4", "E7", "E9", "F", "I"]

# Phase 2: Add common improvements
select = ["E4", "E7", "E9", "F", "I", "N", "UP", "B"]

# Phase 3: Comprehensive ruleset
select = ["ALL"]
ignore = ["E501", "D100", "D101", "D102", "D103"]
```

### Team adoption guidelines

Successful adoption requires **gradual implementation with clear documentation and team training**. Start with essential rules, provide comprehensive editor integration setup, and establish clear CI/CD enforcement policies.

The combination of Ruff and Pydantic-settings represents a modern, efficient approach to Python development that addresses traditional toolchain pain points while providing enterprise-grade capabilities. Their adoption enables significant improvements in developer productivity, code quality, and operational reliability for Python 3.11+ applications.

For teams prioritizing performance, type safety, and maintainability, these tools provide an excellent foundation for modern Python development workflows. The migration path is straightforward, with comprehensive documentation and strong community support making adoption both practical and beneficial.
