# LLM Coding Prompts

A curated collection of concise, instruction-based prompts and production-ready project templates for modern software development with LLMs.

## Overview

This repository provides:

- **Optimized prompts** for Python and Rust development
- **Production-ready templates** with best practices and configurations
- **Post-modification workflows** for maintaining code quality
- **Tool-specific configurations** kept clean and separate

## Project Structure

```
.
├── prompts/           # Language-specific development prompts
│   ├── general.md     # Universal coding guidelines
│   ├── python.md      # Python development with uv, Ruff, and Pydantic
│   └── rust.md        # Rust development with modern tooling
└── templates/         # Project templates
    ├── python/
    │   ├── minimal/       # Basic Python project
    │   └── deep-learning/ # ML/DL project with PyTorch Lightning
    └── rust/
        ├── minimal/       # Single-crate Rust project
        └── workspace/     # Multi-crate workspace project
```

## Quick Start

### Prerequisites

The setup script requires:

- **Fish shell**: [Installation guide](https://fishshell.com/)
- **gum**: Interactive prompt library ([Installation](https://github.com/charmbracelet/gum))

```bash
# Install gum (choose your platform)
brew install gum                   # macOS
sudo apt install gum               # Ubuntu/Debian
winget install charmbracelet.gum   # Windows
```

### Automated Setup (Recommended)

Use the interactive setup script for the fastest onboarding:

```bash
# Clone the repository
git clone <repository-url>
cd LLM-coding-prompts

# Run the interactive setup
./setup.fish
```

The setup script will:

- **Guide you through selections**: Language, template, and AI providers
- **Collect project information**: Name, path, author details, GitHub username
- **Handle VCS configuration**: Git or Jujutsu support with author setup
- **Copy and customize templates**: Automatic placeholder replacement
- **Generate AI prompt files**: Creates provider-specific prompt files
- **Initialize version control**: Sets up your chosen VCS

**Supported AI Providers:**

- **GitHub Copilot**: `.github/copilot-instructions.md`
- **Cursor**: `.cursor/rules/*.mdc` files
- **Gemini CLI**: `GEMINI.md` file
- **Claude Code**: `CLAUDE.md` file

### Manual Setup (Alternative)

If you prefer manual setup:

1. **Copy the template**: Choose the appropriate template for your project type
2. **Replace placeholders**: Update `{{PROJECT_NAME}}`, `{{AUTHOR_NAME}}`, etc.
3. **Copy prompt files**: Use `general.md` + language-specific prompts
4. **Follow the workflows**: Use the post-modification checks after each code change

## Features

### Python Development

- **uv dependency management** (exclusive usage)
- **Ruff linting and formatting** (replaces Black, isort, Flake8)
- **mypy type checking** (strict configuration)
- **Pydantic-settings** for configuration management
- **FastAPI integration** examples
- **Comprehensive testing** with pytest and coverage

### Rust Development

- **Modern Rust syntax** (Edition 2021+)
- **Workspace management** for multi-crate projects
- **Comprehensive linting** with clippy
- **Security-focused** configurations
- **Error handling** patterns (anyhow/thiserror)
- **Async/await** best practices

### Configuration Management

Each tool has its own dedicated configuration file:

- `ruff.toml` - Linting rules
- `mypy.ini` - Type checking
- `pytest.ini` - Testing configuration
- `.coveragerc` - Coverage settings
- `clippy.toml` - Rust linting rules

## Development Workflow

### Post-modification Checks

**Python:**

```bash
uv run ruff check --fix .
uv run ruff format .
uv run mypy .
uv run pytest
```

**Rust:**

```bash
cargo fmt
cargo clippy --all-targets --all-features -- -D warnings
cargo test
```

### Key Principles

1. **Run checks immediately** after each code modification
2. **Zero warnings/errors** required before considering task complete
3. **Use templates** for consistent project structure
4. **Follow prompt guidelines** for best practices

## Template Details

### Python Templates

#### Minimal Template

- Basic Python project structure
- uv dependency management
- Ruff + mypy + pytest configuration
- GitHub Actions CI/CD

#### Deep Learning Template

- PyTorch Lightning integration
- ML-specific linting rules
- Comprehensive testing for ML workflows
- GPU-optimized configurations

### Rust Templates

#### Minimal Template

- Single-crate project
- Essential dependencies (anyhow, thiserror, tracing)
- Security-focused clippy configuration
- Documentation generation

#### Workspace Template

- Multi-crate workspace structure
- Centralized dependency management
- Comprehensive linting and testing
- Security auditing with cargo-audit

## Installation and Setup

### Python Projects

1. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Copy template: `cp -r templates/python/minimal my-project`
3. Initialize: `cd my-project && uv init`
4. Install dependencies: `uv sync`

### Rust Projects

1. Install Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
2. Copy template: `cp -r templates/rust/minimal my-project`
3. Build: `cd my-project && cargo build`

## Best Practices

### Code Quality

- **Immediate feedback**: Run quality checks after each modification
- **Zero tolerance**: No warnings or errors allowed
- **Consistent style**: Use formatters and linters religiously
- **Type safety**: Leverage static analysis tools

### Project Organization

- **Clean configurations**: Each tool has its own config file
- **Template-driven**: Use provided templates for consistency
- **Documentation**: Write clear, concise documentation
- **Testing**: Comprehensive test coverage

## Contributing

1. Keep prompts **concise and instruction-based**
2. Include **concrete examples** when necessary
3. Maintain **clean separation** of configurations
4. Update **both prompts and templates** consistently
5. Test configurations with **real projects**

## Acknowledgements

This project was inspired by and adopts concepts from:

- **[simple-modern-uv](https://github.com/jlevy/simple-modern-uv)** by Joshua Levy - Provided foundational insights on modern Python development practices with uv, Ruff, and related tooling. Several prompt concepts and best practices were adapted from this excellent resource.

## License

MIT License - see LICENSE file for details.

## Notes

- **No Docker configurations**: Development doesn't require containers
- **No pre-commit hooks**: Designed for jujutsu and VCS-agnostic workflows
- **Post-modification focus**: Immediate feedback over automated hooks
- **Production-ready**: All configurations tested in real projects
