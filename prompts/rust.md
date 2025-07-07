# Enhanced Rust Coding Guidelines

These are comprehensive rules for modern Rust development using contemporary tooling and practices.

## Rust Version and Edition

Target Rust Edition 2024+ with the latest stable compiler. Write code that leverages modern Rust features and idioms appropriate for Edition 2024.

Always use modern Rust practices including:

- Advanced type system features (GATs, async traits, etc.)
- Modern control flow constructs (if let chains, let-else)
- Contemporary error handling patterns
- Latest async/await patterns

## Project Setup and Developer Workflows

### Cargo Workspace Structure

**ALWAYS use Cargo Workspaces for any project beyond a single binary.**

For projects with multiple crates, use a flat workspace layout:

```
my_project/
├── Cargo.toml         # Virtual workspace manifest
├── Cargo.lock         # Single lockfile
├── xtask/             # Project automation
│   ├── Cargo.toml
│   └── src/main.rs
├── libs/              # Library crates
│   ├── my_core/
│   │   ├── Cargo.toml
│   │   └── src/lib.rs
│   └── my_utils/
│       ├── Cargo.toml
│       └── src/lib.rs
└── apps/              # Binary crates
    └── my_cli/
        ├── Cargo.toml
        └── src/main.rs
```

### Essential Cargo Commands

Use these standard commands for development:

```bash
# Install/update dependencies
cargo update

# Build with all features and targets
cargo build --all-targets --all-features

# Run comprehensive linting
cargo clippy --all-targets --all-features -- -D warnings

# Format all code
cargo fmt

# Run all tests
cargo test

# Run tests with output
cargo test -- --nocapture

# Check code without building
cargo check --all-targets --all-features
```

### Quality Assurance Workflow

**ALWAYS run these checks before considering any task complete:**

1. `cargo fmt` - Format code
2. `cargo clippy --all-targets --all-features -- -D warnings` - Lint with zero warnings
3. `cargo test` - All tests must pass
4. `cargo check --all-targets --all-features` - Verify compilation

**You must verify zero linter warnings/errors and zero test failures.**

## Modern Rust Idioms and Syntax

### Control Flow

Use modern control flow constructs:

```rust
// PREFER: if let chains (Edition 2024+)
if let Some(user) = get_user() && user.is_active && let Some(permissions) = user.permissions() {
    println!("User has permissions: {:?}", permissions);
}

// PREFER: let-else for early returns
let Some(config) = load_config() else {
    return Err(anyhow!("Failed to load configuration"));
};
```

### Async/Await Patterns

Use modern async patterns:

```rust
// Use async fn in traits (Edition 2024+)
pub trait AsyncService {
    async fn fetch(&self, url: &str) -> Result<String>;
}

// Use async closures
let task = async || {
    perform_async_work().await
};
```

### Error Handling Strategy

**For Libraries**: Use `thiserror` for structured error types:

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum DataStoreError {
    #[error("Connection failed")]
    ConnectionError(#[from] std::io::Error),

    #[error("Record not found: {0}")]
    NotFound(String),

    #[error("Invalid data format")]
    InvalidFormat(#[from] serde_json::Error),
}
```

**For Applications**: Use `anyhow` for error propagation:

```rust
use anyhow::{Context, Result};

fn load_config() -> Result<Config> {
    let content = std::fs::read_to_string("config.toml")
        .context("Failed to read configuration file")?;

    let config: Config = toml::from_str(&content)
        .context("Failed to parse configuration")?;

    Ok(config)
}
```

## Code Organization and Modules

### Module Structure

- Start with code in `lib.rs` or `main.rs`
- Create modules only when files exceed ~1000 lines OR when clear logical boundaries emerge
- Use modules for encapsulation and API design, not premature organization
- Always use `pub(crate)` for internal APIs that need cross-module access

### Import Conventions

```rust
// Group imports: std, external crates, local crates
use std::collections::HashMap;
use std::path::Path;

use serde::{Deserialize, Serialize};
use tokio::fs;

use crate::config::Config;
use crate::utils::validate_path;
```

## Type System Best Practices

### Modern Type Syntax

```rust
// PREFER: Modern generic syntax
fn process_items<T>(items: impl Iterator<Item = T>) -> Vec<T>
where
    T: Clone + Send,
{
    items.collect()
}

// PREFER: Associated types and GATs where appropriate
trait AsyncIterator {
    type Item;
    type Future<'a>: std::future::Future<Output = Option<Self::Item>>
    where
        Self: 'a;

    fn next(&mut self) -> Self::Future<'_>;
}
```

### Derive Macros and Attributes

Use comprehensive derive macros:

```rust
#[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
pub struct User {
    pub id: u64,
    pub name: String,
    pub email: String,
}
```

## Testing Strategy

### Test Organization

**Unit Tests**: Place in `#[cfg(test)]` modules within the same file:

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_user_creation() {
        let user = User::new("Alice", "alice@example.com");
        assert_eq!(user.name, "Alice");
        assert_eq!(user.email, "alice@example.com");
    }
}
```

**Integration Tests**: Place in `tests/` directory for testing public APIs.

**Documentation Tests**: Write runnable examples in doc comments:

````rust
/// Validates an email address format.
///
/// # Examples
///
/// ```
/// use mylib::validate_email;
///
/// assert!(validate_email("user@example.com").is_ok());
/// assert!(validate_email("invalid-email").is_err());
/// ```
pub fn validate_email(email: &str) -> Result<(), ValidationError> {
    // Implementation
}
````

### Advanced Testing

For complex or critical code, use:

- **Property-based testing** with `proptest` crate
- **Fuzz testing** with `cargo-fuzz`
- **Benchmark testing** with `criterion` crate

## Documentation Standards

### Documentation Comments

````rust
/// A high-level summary of what this function does.
///
/// More detailed explanation of the behavior, including any important
/// implementation details or usage considerations.
///
/// # Arguments
///
/// * `path` - The file path to process
/// * `options` - Configuration options for processing
///
/// # Returns
///
/// Returns the processed data as a `String`, or an error if processing fails.
///
/// # Examples
///
/// ```
/// use mylib::process_file;
///
/// let result = process_file("data.txt", &Default::default())?;
/// assert!(!result.is_empty());
/// ```
///
/// # Errors
///
/// This function will return an error if:
/// - The file cannot be read
/// - The file contains invalid data
///
/// # Panics
///
/// This function panics if the path contains null bytes.
pub fn process_file(path: &Path, options: &ProcessOptions) -> Result<String, ProcessError> {
    // Implementation
}
````

### Documentation Sections

Use standard sections when applicable:

- `# Examples` (mandatory for most public APIs)
- `# Errors` (for fallible functions)
- `# Panics` (if the function can panic)
- `# Safety` (for unsafe functions)

## Performance and Safety

### Memory Management

```rust
// PREFER: Smart pointers over raw pointers
use std::sync::Arc;
use std::rc::Rc;

// Use appropriate smart pointer for the use case
let shared_data: Arc<Data> = Arc::new(data);

// PREFER: Borrow checker friendly patterns
fn process_data(data: &[u8]) -> Result<Vec<u8>, ProcessError> {
    // Work with borrowed data when possible
}
```

### Unsafe Code

When unsafe code is necessary:

```rust
/// # Safety
///
/// This function is unsafe because it dereferences a raw pointer.
/// The caller must ensure that:
/// - `ptr` is valid and properly aligned
/// - `ptr` points to a valid `T`
/// - No other code is mutating the data at `ptr`
pub unsafe fn read_raw<T>(ptr: *const T) -> T {
    std::ptr::read(ptr)
}
```

## Project Automation

### Use cargo-xtask

Create an `xtask` crate for project automation:

```rust
// xtask/src/main.rs
use std::process::Command;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let task = std::env::args().nth(1);

    match task.as_deref() {
        Some("lint") => {
            run_command("cargo", &["fmt", "--check"])?;
            run_command("cargo", &["clippy", "--all-targets", "--all-features", "--", "-D", "warnings"])?;
        }
        Some("test") => {
            run_command("cargo", &["test", "--all-targets", "--all-features"])?;
        }
        Some("ci") => {
            run_command("cargo", &["xtask", "lint"])?;
            run_command("cargo", &["xtask", "test"])?;
        }
        _ => {
            eprintln!("Usage: cargo xtask <lint|test|ci>");
            std::process::exit(1);
        }
    }

    Ok(())
}

fn run_command(cmd: &str, args: &[&str]) -> Result<(), Box<dyn std::error::Error>> {
    let status = Command::new(cmd).args(args).status()?;
    if !status.success() {
        std::process::exit(1);
    }
    Ok(())
}
```

## Dependency Management

### Workspace Dependencies

Centralize dependency versions in workspace `Cargo.toml`:

```toml
[workspace]
members = ["apps/*", "libs/*", "xtask"]
resolver = "2"

[workspace.dependencies]
# External dependencies
serde = { version = "1.0", features = ["derive"] }
tokio = { version = "1", features = ["full"] }
anyhow = "1.0"
thiserror = "1.0"

# Internal dependencies
my_core = { path = "libs/my_core" }
my_utils = { path = "libs/my_utils" }
```

### Feature Management

Use features judiciously:

```toml
[features]
default = ["std"]
std = []
serde = ["dep:serde"]
async = ["dep:tokio"]
```

## Code Quality Guidelines

### Comments and Documentation

- Comments should explain **WHY**, not **WHAT**
- Avoid obvious comments that repeat the code
- Use `//!` for module-level documentation
- Use `///` for item-level documentation

### Code Style

- Use `rustfmt` with default settings
- Follow clippy suggestions religiously
- Prefer explicit over implicit when it improves clarity
- Use descriptive variable names
- Keep functions focused and relatively short

### Error Handling

```rust
// PREFER: Explicit error handling
fn process_data(data: &str) -> Result<ProcessedData, ProcessError> {
    let parsed = parse_data(data)
        .map_err(|e| ProcessError::ParseError(e.to_string()))?;

    validate_data(&parsed)
        .map_err(|e| ProcessError::ValidationError(e.to_string()))?;

    Ok(transform_data(parsed))
}

// AVOID: Unwrapping without good reason
fn bad_process_data(data: &str) -> ProcessedData {
    let parsed = parse_data(data).unwrap(); // Don't do this!
    transform_data(parsed)
}
```

## Performance Considerations

### Allocation Management

```rust
// PREFER: Minimize allocations
fn process_lines(input: &str) -> Vec<String> {
    let mut results = Vec::with_capacity(input.lines().count());

    for line in input.lines() {
        if !line.is_empty() {
            results.push(line.trim().to_string());
        }
    }

    results
}

// PREFER: Use iterators for lazy evaluation
fn find_valid_entries(data: &[Entry]) -> impl Iterator<Item = &Entry> {
    data.iter().filter(|entry| entry.is_valid())
}
```

### Async Best Practices

```rust
// PREFER: Structured concurrency
async fn process_multiple_urls(urls: &[&str]) -> Result<Vec<String>, reqwest::Error> {
    let futures = urls.iter().map(|url| fetch_url(url));

    let results = futures::future::try_join_all(futures).await?;
    Ok(results)
}

// PREFER: Proper error handling in async code
async fn fetch_with_retry(url: &str, max_retries: u32) -> Result<String, NetworkError> {
    let mut attempts = 0;

    loop {
        match fetch_url(url).await {
            Ok(data) => return Ok(data),
            Err(e) if attempts < max_retries => {
                attempts += 1;
                tokio::time::sleep(Duration::from_secs(2_u64.pow(attempts))).await;
            }
            Err(e) => return Err(NetworkError::MaxRetriesExceeded(e)),
        }
    }
}
```

## Continuous Integration

### CI Configuration

Ensure your CI pipeline runs:

```bash
# Format check
cargo fmt --check

# Lint with warnings as errors
cargo clippy --all-targets --all-features -- -D warnings

# Test with all features
cargo test --all-targets --all-features

# Documentation build
cargo doc --all-features --no-deps

# Security audit
cargo audit
```

## Migration and Compatibility

### Edition Migration

When upgrading Rust editions:

1. Update `Cargo.toml` edition field
2. Run `cargo fix --edition` to automatically fix compatibility issues
3. Update code to use new edition idioms
4. Test thoroughly with the new edition

### API Evolution

For library crates:

- Use `#[deprecated]` attribute for deprecation warnings
- Follow semantic versioning strictly
- Document breaking changes in CHANGELOG
- Consider using feature flags for experimental APIs

## Security Considerations

### Input Validation

```rust
use std::path::Path;

fn safe_file_operation(path: &str) -> Result<String, std::io::Error> {
    let path = Path::new(path);

    // Validate path to prevent directory traversal
    if path.components().any(|component| matches!(component, std::path::Component::ParentDir)) {
        return Err(std::io::Error::new(
            std::io::ErrorKind::InvalidInput,
            "Path contains parent directory references"
        ));
    }

    std::fs::read_to_string(path)
}
```

### Dependency Security

- Regularly run `cargo audit` to check for security vulnerabilities
- Keep dependencies updated
- Minimize dependency count
- Review dependencies for security implications

This comprehensive guide ensures modern, idiomatic, and maintainable Rust code that leverages the latest language features and best practices.
