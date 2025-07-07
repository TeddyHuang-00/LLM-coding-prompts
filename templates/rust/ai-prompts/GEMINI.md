# Rust Project Configuration

## Language and Edition
- Use Rust 2021 edition exclusively with modern syntax and idioms
- Use latest stable Rust features and patterns
- Use modern control flow: if let chains, let-else patterns, match expressions
- Use async/await for I/O operations with tokio runtime

## Tooling and Development Environment
- Use cargo fmt for all code formatting (standard Rust formatting)
- Use cargo clippy with zero warnings policy for linting
- Use cargo test for comprehensive testing
- Use cargo check for compilation verification
- Use cargo build for project building

## Code Style Standards
- Use snake_case for variables and functions
- Use PascalCase for types and traits
- Use SCREAMING_SNAKE_CASE for constants
- Use descriptive variable names and avoid abbreviations
- Use proper indentation and formatting

## Error Handling Strategy
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
- **serde**: For serialization with derive macros
- **tracing**: For structured logging instead of println! in production code
- **clap**: With derive API for command-line argument parsing
- **tokio**: For async runtime and I/O operations
- **anyhow**: For application error handling
- **thiserror**: For library error types
- **criterion**: For benchmarking performance-critical code

## Project Structure
- Use workspace structure for multi-crate projects
- Use modules for code organization and encapsulation
- Use pub(crate) for internal APIs that need cross-module access
- Use feature flags for optional functionality
- Use semantic versioning for crate releases

## Async Programming
- Use async/await patterns for I/O operations with tokio runtime
- Use async traits for async behavior
- Use proper async error handling patterns
- Use structured concurrency patterns
- Use channels for message passing between async tasks

## Testing Strategy
- Use #[cfg(test)] modules for unit tests
- Use assert! and assert_eq! for test assertions
- Use integration tests in tests/ directory
- Use property-based testing with proptest for complex logic
- Use mock objects and test doubles for external dependencies
- Maintain comprehensive test coverage

## Quality Assurance Workflow
Before committing code, ALWAYS run these commands in order:
1. `cargo fmt` - Format code
2. `cargo clippy --all-targets --all-features -- -D warnings` - Lint with zero warnings
3. `cargo test` - Run all tests
4. `cargo check --all-targets --all-features` - Verify compilation

All steps must pass without errors or warnings.

## Documentation
- Use documentation comments /// for public APIs
- Write comprehensive examples in doc comments
- Use #[doc(hidden)] for internal implementation details
- Use type aliases for complex types to improve readability
- Document error conditions and panic scenarios

## Performance and Safety
- Use iterators and functional programming patterns where appropriate
- Use lifetime annotations only when necessary, prefer owned types
- Avoid unsafe code unless absolutely necessary
- Use #[inline] for performance-critical small functions
- Use const fn for compile-time evaluation when possible
- Use smart pointers (Arc, Rc) for shared ownership

## Memory Management
- Use Box<T> for heap allocation when needed
- Use Cow<T> for clone-on-write semantics
- Use proper lifetime management
- Avoid memory leaks and dangling pointers
- Use RAII patterns for resource management

## Concurrency
- Use channels for message passing between threads
- Use mutexes and RwLocks for shared state
- Use atomic types for lock-free programming
- Use rayon for data parallelism
- Use proper synchronization primitives

## Build Commands
- `cargo build` - Build the project
- `cargo run` - Run the application
- `cargo test` - Run test suite
- `cargo fmt` - Format code
- `cargo clippy --all-targets --all-features -- -D warnings` - Lint code
- `cargo check --all-targets --all-features` - Check compilation
- `cargo bench` - Run benchmarks