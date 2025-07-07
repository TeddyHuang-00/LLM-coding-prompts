# Rust Project Configuration

## Language and Edition
- Use Rust 2021 edition exclusively with modern syntax and idioms
- Use latest stable Rust features and patterns
- Use modern control flow: if let chains, let-else patterns, match expressions
- Use async/await for I/O operations with tokio runtime

## Tooling and Development
- Use cargo fmt for all code formatting (standard Rust formatting)
- Use cargo clippy with zero warnings policy for linting
- Use cargo test for comprehensive testing
- Use cargo check for compilation verification

## Code Style
- Use snake_case for variables and functions
- Use PascalCase for types and traits
- Use SCREAMING_SNAKE_CASE for constants
- Use descriptive variable names and avoid abbreviations

## Error Handling
- Use thiserror for library error types with structured error handling
- Use anyhow for application error handling and error propagation
- Use Result<T, E> for error handling, avoid unwrap() in production code
- Use proper error propagation with ? operator
- Use let-else patterns for early returns and error handling

## Data Types and Collections
- Use String for owned strings, &str for borrowed strings
- Use Vec<T> for dynamic collections instead of arrays
- Use HashMap and BTreeMap for key-value storage
- Use PathBuf for owned paths, &Path for borrowed paths
- Use generic types and traits for code reuse and flexibility
- Use #[derive(Debug, Clone, PartialEq)] for common traits

## Essential Dependencies
- Use serde for serialization with derive macros
- Use tracing for structured logging instead of println! in production code
- Use clap with derive API for command-line argument parsing
- Use tokio for async runtime and I/O operations
- Use anyhow for application error handling
- Use thiserror for library error types

## Project Structure
- Use workspace structure for multi-crate projects
- Use modules for code organization and encapsulation
- Use pub(crate) for internal APIs that need cross-module access
- Use feature flags for optional functionality

## Async Programming
- Use async/await patterns for I/O operations with tokio runtime
- Use async traits for async behavior
- Use proper async error handling patterns
- Use structured concurrency patterns

## Testing
- Use #[cfg(test)] modules for unit tests
- Use assert! and assert_eq! for test assertions
- Use integration tests in tests/ directory
- Use criterion for benchmarking performance-critical code

## Quality Assurance
- Run cargo fmt before committing code
- Run cargo clippy --all-targets --all-features -- -D warnings before committing
- Run cargo test to verify all tests pass
- Run cargo check --all-targets --all-features for compilation verification
- Maintain zero linting warnings and compilation errors

## Documentation
- Use documentation comments /// for public APIs
- Write comprehensive examples in doc comments
- Use type aliases for complex types to improve readability
- Document error conditions and panic scenarios

## Performance and Safety
- Use iterators and functional programming patterns where appropriate
- Use lifetime annotations only when necessary, prefer owned types
- Avoid unsafe code unless absolutely necessary
- Use smart pointers (Arc, Rc) for shared ownership
- Use proper memory management patterns

## Build Commands
- `cargo build` - Build the project
- `cargo run` - Run the application
- `cargo test` - Run test suite
- `cargo fmt` - Format code
- `cargo clippy --all-targets --all-features -- -D warnings` - Lint code
- `cargo check --all-targets --all-features` - Check compilation