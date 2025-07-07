# {{PROJECT_NAME}}_core

Core functionality and types for the {{PROJECT_NAME}} project.

## Features

- `std` (default): Standard library support

## Usage

```rust
use {{PROJECT_NAME}}_core::{core, types::Config, Result};

// Initialize the core system
core::init()?;

// Use configuration
let config = Config::default();
println!("App name: {}", config.name);
```

## Error Handling

The crate provides a comprehensive error type that covers common error scenarios:

```rust
use {{PROJECT_NAME}}_core::{Error, Result};

fn example_function() -> Result<()> {
    // Your code here
    Ok(())
}
```