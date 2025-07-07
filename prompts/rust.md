# Rust Development Guide

Use Rust Edition 2024+ with latest stable compiler and modern idioms.

## Quick Start

```bash
# Check code quality
cargo fmt
cargo clippy --all-targets --all-features -- -D warnings
cargo test

# Build and run
cargo build --release
cargo run
```

## Essential Commands

```bash
cargo update                                    # Update dependencies
cargo check --all-targets --all-features       # Quick compilation check
cargo build --all-targets --all-features       # Build everything
cargo test -- --nocapture                      # Test with output
```

## Project Structure

### Workspace Layout

Use workspaces for multi-crate projects:

```
my_project/
├── Cargo.toml         # Workspace manifest
├── libs/              # Library crates
│   └── my_core/
│       ├── Cargo.toml
│       └── src/lib.rs
├── apps/              # Binary crates
│   └── my_cli/
│       ├── Cargo.toml
│       └── src/main.rs
└── xtask/             # Automation
    ├── Cargo.toml
    └── src/main.rs
```

### Project Configuration

**ALWAYS use workspace dependencies for multi-crate projects.**

Use the project templates which include complete configurations for:
- Workspace dependencies and structure
- Clippy lints and cargo configuration
- CI/CD setup with comprehensive testing
- Required dependencies for error handling, logging, and security

### Quality Checks

**ALWAYS run these checks before considering any task complete:**

```bash
cargo fmt                                         # Format
cargo clippy --all-targets --all-features -- -D warnings  # Lint (zero warnings required)
cargo test                                       # Test (all tests must pass)
cargo check --all-targets --all-features        # Compile check
```

**You must verify zero linter warnings/errors and zero test failures.**

### Post-modification Workflow

**ALWAYS run these checks immediately after making any code changes:**

```bash
# Full quality check after each modification
cargo fmt && cargo clippy --all-targets --all-features -- -D warnings && cargo test

# Alternative: Use xtask for automation
cargo xtask ci
```

## Modern Rust Syntax

### Control Flow

```rust
// if let chains (Edition 2024+)
if let Some(user) = get_user() && user.is_active && let Some(perms) = user.permissions() {
    println!("User has permissions: {:?}", perms);
}

// let-else for early returns
let Some(config) = load_config() else {
    return Err(anyhow!("Failed to load configuration"));
};
```

### Async Patterns

```rust
// Async functions in traits
pub trait AsyncService {
    async fn fetch(&self, url: &str) -> Result<String>;
}

// Async closures
let task = async || perform_async_work().await;
```

### Error Handling

**Libraries**: Use `thiserror`

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataStoreError {
    #[error("Connection failed")]
    ConnectionError(#[from] std::io::Error),

    #[error("Record not found: {0}")]
    NotFound(String),
}
```

**Applications**: Use `anyhow`

```rust
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("Failed to read config file")?;

    toml::from_str(&content).context("Failed to parse config")
}
```

## Code Organization

### Module Structure

Start with `lib.rs` or `main.rs`. Create modules only when files exceed ~1000 lines or clear boundaries emerge.

```rust
// Import grouping: std, external, local
use std::collections::HashMap;
use std::path::Path;

use serde::{Deserialize, Serialize};
use tokio::fs;

use crate::config::Config;
```

### Common Types

```rust
// Use impl Trait for flexibility
fn process_items<T>(items: impl Iterator<Item = T>) -> Vec<T>
where
    T: Clone + Send,
{
    items.collect()
}

// Comprehensive derives
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct User {
    pub id: u64,
    pub name: String,
    pub email: String,
}
```

## Testing

### Test Organization

**Unit tests**: In `#[cfg(test)]` modules

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_user_creation() {
        let user = User::new("Alice", "alice@example.com");
        assert_eq!(user.name, "Alice");
    }
}
```

**Integration tests**: In `tests/` directory

**Doc tests**: In doc comments

````rust
/// Validates email format.
///
/// ```
/// use mylib::validate_email;
/// assert!(validate_email("user@example.com").is_ok());
/// ```
pub fn validate_email(email: &str) -> Result<(), ValidationError> {
    // Implementation
}
````

### Advanced Testing

- `proptest` for property-based testing
- `cargo-fuzz` for fuzz testing
- `criterion` for benchmarks

## Documentation

### Doc Comments

````rust
/// Brief summary of what this function does.
///
/// # Arguments
/// * `path` - File path to process
/// * `options` - Configuration options
///
/// # Examples
/// ```
/// use mylib::process_file;
/// let result = process_file("data.txt", &Default::default())?;
/// ```
///
/// # Errors
/// Returns error if file cannot be read or contains invalid data.
pub fn process_file(path: &Path, options: &ProcessOptions) -> Result<String, ProcessError> {
    // Implementation
}
````

### Required Sections

- `# Examples` (for public APIs)
- `# Errors` (for fallible functions)
- `# Panics` (if function can panic)
- `# Safety` (for unsafe functions)

## Performance & Safety

### Memory Management

```rust
// Use appropriate smart pointers
let shared_data: Arc<Data> = Arc::new(data);

// Prefer borrowing
fn process_data(data: &[u8]) -> Result<Vec<u8>, ProcessError> {
    // Work with borrowed data when possible
}
```

### Unsafe Code

```rust
/// # Safety
/// Caller must ensure `ptr` is valid and properly aligned.
pub unsafe fn read_raw<T>(ptr: *const T) -> T {
    std::ptr::read(ptr)
}
```

## Project Automation

### XTask Setup

Create automation crate:

```rust
// xtask/src/main.rs
use std::process::Command;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    match std::env::args().nth(1).as_deref() {
        Some("lint") => {
            run_cmd("cargo", &["fmt", "--check"])?;
            run_cmd("cargo", &["clippy", "--all-targets", "--all-features", "--", "-D", "warnings"])?;
        }
        Some("test") => run_cmd("cargo", &["test", "--all-targets", "--all-features"])?,
        Some("ci") => {
            run_cmd("cargo", &["xtask", "lint"])?;
            run_cmd("cargo", &["xtask", "test"])?;
        }
        _ => {
            eprintln!("Usage: cargo xtask <lint|test|ci>");
            std::process::exit(1);
        }
    }
    Ok(())
}

fn run_cmd(cmd: &str, args: &[&str]) -> Result<(), Box<dyn std::error::Error>> {
    let status = Command::new(cmd).args(args).status()?;
    if !status.success() {
        std::process::exit(1);
    }
    Ok(())
}
```

## CI/CD & Development

Use the project templates which include complete configurations for:
- GitHub Actions CI/CD with comprehensive testing
- Security auditing and dependency checking
- Documentation generation and testing

## Best Practices

### Code Quality

- **ALWAYS run quality checks after each modification**:
  ```bash
  cargo fmt && cargo clippy --all-targets --all-features -- -D warnings && cargo test
  ```
- **Run these checks immediately after making any code changes**
- Comments explain WHY, not WHAT
- Use `rustfmt` with default settings
- Follow all clippy suggestions
- Keep functions focused and short

### Error Handling

```rust
// Good: Explicit error handling
fn process_data(data: &str) -> Result<ProcessedData, ProcessError> {
    let parsed = parse_data(data)
        .map_err(|e| ProcessError::ParseError(e.to_string()))?;

    validate_data(&parsed)
        .map_err(|e| ProcessError::ValidationError(e.to_string()))?;

    Ok(transform_data(parsed))
}

// Bad: Unwrapping
fn bad_process_data(data: &str) -> ProcessedData {
    let parsed = parse_data(data).unwrap(); // Don't do this!
    transform_data(parsed)
}
```

### Performance Tips

- Pre-allocate vectors when size is known
- Use iterators for lazy evaluation
- Prefer borrowing over cloning
- Use `Arc` for shared data across threads

### Security

**ALWAYS follow these security practices:**

- Validate all input at boundaries
- Run `cargo audit` regularly to check for vulnerabilities
- Minimize dependencies and review them for security
- Avoid directory traversal attacks
- Use `SecretString` for sensitive data
- Enable security-focused clippy lints

```rust
use secrecy::{ExposeSecret, SecretString};

// Validate paths to prevent directory traversal
fn validate_path(path: &Path) -> Result<(), std::io::Error> {
    if path.components().any(|c| matches!(c, std::path::Component::ParentDir)) {
        return Err(std::io::Error::new(
            std::io::ErrorKind::InvalidInput,
            "Path contains parent directory references"
        ));
    }
    Ok(())
}

// Use SecretString for sensitive data
fn handle_password(password: SecretString) {
    // Use password.expose_secret() only when needed
    authenticate_user(password.expose_secret());
}
```

### Required Dependencies

**ALWAYS include these dependencies in your projects:**
- `anyhow` for application error handling
- `thiserror` for library error types
- `secrecy` for sensitive data handling
- `tracing` and `tracing-subscriber` for logging
- `tokio-test` for async testing

Use the project templates which include complete dependency configurations with proper workspace setup.
