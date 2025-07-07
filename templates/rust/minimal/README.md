# {{PROJECT_NAME}}

A modern Rust project template with best practices and comprehensive tooling.

## Setup

1. **Install Rust using rustup**:
   ```bash
   rustup show # Should show the active toolchain
   ```
2. **Clone and build**:
   ```bash
   git clone https://github.com/{{GITHUB_NAME}}/{{PROJECT_NAME}}.git
   cd {{PROJECT_NAME}}
   cargo build
   ```

## Development

### Essential Commands

```bash
# Build the project
cargo build

# Run the application
cargo run

# Run tests
cargo test

# Format code
cargo fmt

# Lint code
cargo clippy --all-targets --all-features -- -D warnings

# Check without building
cargo check --all-targets --all-features

# Run benchmarks
cargo bench
```

### Quality Assurance

Before committing, always run:

```bash
# Format code
cargo fmt

# Lint with zero warnings
cargo clippy --all-targets --all-features -- -D warnings

# Run all tests
cargo test

# Verify compilation
cargo check --all-targets --all-features
```

## Project Structure

```
{{PROJECT_NAME}}/
├── src/
│   └── main.rs         # Main entry point
├── tests/              # Integration tests
├── benches/            # Benchmarks
├── Cargo.toml          # Project manifest
├── .gitignore          # Git ignore patterns
└── README.md           # This file
```

## Configuration

The project uses `Cargo.toml` for configuration:

- **Dependencies**: Modern Rust crates for common functionality
- **Linting**: Comprehensive clippy rules for code quality
- **Profiles**: Optimized release and development builds
- **Workspace**: Single-crate workspace setup

## Dependencies

- **anyhow**: Flexible error handling
- **clap**: Command-line argument parsing
- **serde**: Serialization/deserialization
- **tokio**: Async runtime
- **tracing**: Structured logging
- **criterion**: Benchmarking (dev dependency)

## Best Practices

This template follows modern Rust best practices:

- **Safety**: Forbids unsafe code
- **Performance**: Optimized release builds
- **Error Handling**: Comprehensive error management
- **Testing**: Unit and integration tests
- **Documentation**: Clear code documentation
- **Tooling**: Automated formatting and linting

## License

Licensed under either of

- Apache License, Version 2.0 ([LICENSE-APACHE](LICENSE-APACHE) or http://www.apache.org/licenses/LICENSE-2.0)
- MIT license ([LICENSE-MIT](LICENSE-MIT) or http://opensource.org/licenses/MIT)

at your option.
