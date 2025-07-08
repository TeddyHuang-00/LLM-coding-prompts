# {{PROJECT_NAME}} - Rust Workspace Project

A modern Rust workspace project template with multiple crates, build automation, and best practices.

## Project Structure

```
{{PROJECT_NAME}}/
├── Cargo.toml           # Workspace configuration
├── Cargo.lock           # Dependency lockfile
├── README.md
├── libs/                # Library crates
│   ├── {{PROJECT_NAME}}_core/           # Core functionality
│   └── {{PROJECT_NAME}}_utils/          # Utility functions
├── apps/                # Binary crates
│   └── {{PROJECT_NAME}}_cli/            # Command-line interface
└── xtask/               # Build automation
```

## Features

- **Workspace Configuration**: Centralized dependency management
- **Multiple Crates**: Organized into libraries and applications
- **Build Automation**: xtask for common development tasks
- **Modern Rust**: Edition 2024+ with latest best practices
- **Quality Assurance**: Comprehensive linting and testing setup

## Quick Start

### Prerequisites

- Rust 1.75+ (Edition 2024 support)
- Cargo

### Building

```bash
# Build all crates
cargo build --all-targets --all-features

# Run the CLI application
cargo run --bin {{PROJECT_NAME}} -- --help
```

### Development

```bash
# Format code
cargo fmt

# Run lints
cargo clippy --all-targets --all-features -- -D warnings

# Run tests
cargo test

# Run complete CI pipeline
cargo xtask ci
```

### Available Commands

The xtask automation provides common development tasks:

```bash
cargo xtask ci      # Run complete CI pipeline
cargo xtask fmt     # Format code
cargo xtask lint    # Run clippy lints
cargo xtask test    # Run tests
cargo xtask build   # Build all crates
cargo xtask clean   # Clean build artifacts
```

## Crate Overview

### {{PROJECT_NAME}}_core

Core functionality and types used throughout the project.

**Features:**
- `std` (default): Standard library support

### {{PROJECT_NAME}}_utils

Common utility functions and helpers.

**Features:**
- `std` (default): Standard library support

### {{PROJECT_NAME}}_cli

Command-line interface for the project.

**Usage:**
```bash
# Initialize a new project
cargo run --bin {{PROJECT_NAME}} init --name my_project

# Run the application
cargo run --bin {{PROJECT_NAME}} run --input data.txt

# Check status
cargo run --bin {{PROJECT_NAME}} status
```

## Development Guidelines

### Code Quality

- All code must pass `cargo clippy` with zero warnings
- Code must be formatted with `cargo fmt`
- All tests must pass
- New features should include tests

### Adding Dependencies

Add dependencies to the workspace `Cargo.toml` and reference them in individual crates:

```toml
# In workspace Cargo.toml
[workspace.dependencies]
new_dependency = "1.0"

# In individual crate Cargo.toml
[dependencies]
new_dependency = { workspace = true }
```

### Features

Use features to enable optional functionality:

```toml
[features]
default = ["std"]
std = []
optional_feature = ["dep:optional_dependency"]
```

## License

{{LICENSE_TEXT}}

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the CI pipeline: `cargo xtask ci`
5. Submit a pull request